# Copyright (c) 2017, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the name of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from docutils.writers import Writer
from docutils.nodes import NodeVisitor
from .nodeconfig import active_nodes, skip_node, pass_node
import re

#############################
# Book Writer
class BookWriter(Writer):
    
    # Initialize Class
    def __init__(self, builder, config):
        Writer.__init__(self)
        self.config = config
        self.builder = builder

    # Translator
    def translate(self):
        translator = BookTranslator(self.document, self.config)
        self.document.walkabout(translator)
        self.output = translator.astext()

#############################
# Book Translator
class BookTranslator(NodeVisitor):

    def __init__(self, document, config):
        NodeVisitor.__init__(self, document)
        self.config = config
        self.build = 'bacch'
        self.head = []
        self.body = []
        self.current = ''
        self.title_list = {}
        self.titlecall = None
        self.open_paragraph = False
        self.sections = ['chapter', 'section', 'subsection', 
                'subsubsection', 'paragraph', 'subparagraph']
        self.section_level = -2 

        # Configure Nodes
        for (name, job) in active_nodes:
            if job == 'skip':
                setattr(self, 'visit_%s' % name, skip_node)
            elif job == 'pass':
                setattr(self, 'visit_%s' % name, pass_node)
                setattr(self, 'depart_%s' % name, pass_node)
            else:
                raise ValueError("Error Node Handler: %s" % name)

    def astext(self):
        return '%s\n\n%s' % (
                '\n'.join(self.head),
                ''.join(self.body))

    ########################
    # Structural Nodes

    # Document
    def visit_document(self, node):
        self.body.append('\n\\begin{document}\n')

        # Document Options
        options = getattr(self.config, '%s_options' % self.build)
        if options is not None:
            doc = '\\documentclass[%s]{book}\n' % ','.join(options)
        else:
            doc = '\\documentclass{book}\n'
        self.head.append(doc)

        # Configure Packages
        global_packages = self.config.bacch_gnomon_packages
        local_packages = getattr(self.config, '%s_packages' % self.build)
        packages = {**global_packages, **local_packages}

        if packages != {}:
            for package,options in packages.items():
                if options is None:
                    self.head.append("\\usepackage{%s}" % package)
                else:
                    self.head.append(
                            "\\usepackage[%s]{%s}" % (",".join(options), package))

        # Configure Document
        global_conf = self.config.bacch_gnomon_config
        local_conf = getattr(self.config, '%s_config' % self.build)
        conf = global_conf + local_conf
        if conf != []:
            for line in conf:
                self.head.append(line)

       
    def depart_document(self, node):
        self.body.append('\n\\end{document}')



    # Section
    def visit_section(self, node):
        self.section_level += 1
        title = node.next_node().astext()

        if self.section_level == -1:
            self.title_page(title)
        else:
            text = "\\%s*{%s}\n" % (self.sections[self.section_level], title)
            self.body.append(text)

        # Configure Variables
        self.open_paragraph = True
        if self.section_level == 1:
            self.current = 'section'
        elif self.section_level == 2:
            self.current = 'subsection'

        # Manage Titlelist
        if self.section_level == 1:
            self.titlecall = "\\the%s" % re.sub(' ', '', title)
            self.title_list[self.titlecall] = [title]

            if getattr(self.config, '%s_showtitlelist' % self.build):

                form = getattr(self.config, '%s_showtitlelist_format' % self.build)
                if 'before' in form:
                    self.body.append(form['before'])
                self.body.append('\n%s' % self.titlecall)
                if 'after' in form:
                    self.body.append(form['after'])

        elif self.section_level > 1:
            self.title_list[self.titlecall].append(title)


    def title_page(self, title):

        self.head.append('\\newcommand{\\showtitle}{%s}' % title)

        # Title Page
        titlepage = getattr(self.config, '%s_titlepage' % self.build)
        if titlepage is not None:
            self.body.append(titlepage)

        # Table of Contents
        if getattr(self.config, '%s_toc' % self.build):
            self.body.append('\\tableofcontents\n')


    def depart_section(self, node):
        if self.section_level == 1:
            command = "\\newcommand{%s}{%s.}" % (
                    self.titlecall,
                    "---".join(self.title_list[self.titlecall]))
            self.head.append(command)
        self.section_level += -1

    # Paragraph
    def visit_paragraph(self, node):
        self.body.append('\n')

        if self.open_paragraph:
            self.body.append('\\noindent ')

    def depart_paragraph(self, node):
        self.body.append('\n')

    # Text
    def visit_Text(self, node):
        if self.open_paragraph:
            self.open_paragraph = False

            text = self.lettrine(node.astext())
            self.body.append(text)

        else:
            self.body.append(node.astext())

    def lettrine(self, text):

        base = text.split(' ')
        if self.section_level == 3:
            options = ['lines=1']
            base[0] = '\\lettrine[%s]{}{%s' % (','.join(options), base[0])
            base = self.depart_lettrine(base)
        elif self.section_level <= 3:
            options = ['lines=2']
            if base[0] != '"' or base[0] != "'":
                base[0] = '\\lettrine[%s]{%s}{%s' % (
                        ','.join(options), base[0][0], base[0][1:])
            else:
                base[0] = '\\lettrine[%s]{%s%s}{%s' % (
                        ','.join(options), base[0][0], base[0][1], base[0][2:])
            base = self.depart_lettrine(base)
        return ' '.join(base)

    def depart_lettrine(self, base):

        if len(base) > 3:
            base[2] = base[2] + '}'
        else:
            base[-1] = base[-1] + '}'

        return base 
             


    def depart_Text(self, node):
        pass

    # Title
    def visit_title(self, node):
        self.body.append("Title: ")

    def depart_title(self, node):
        pass

    ##########################
    # Block Markup



    ##########################
    # Inline Markup

    # Strong
    def visit_strong(self, node):
        self.body.append('\\textbf{')

    def depart_strong(self, node):
        self.body.append('}')

    # Emphasis
    def visit_emphasis(self, node):
        self.body.append("\\emph{")

    def depart_emphasis(self, node):
        self.body.append("}")


