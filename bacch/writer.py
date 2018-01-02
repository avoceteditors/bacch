""" Provides the PDF Writer and Translator for both Bacch
and Gnomon builders """
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
import jinja2 as jinja

from .core import active_nodes, skip_node, pass_node


##############################
# LaTeX Writer Class
class LaTeXWriter(Writer):

    # Initialization
    def __init__(self, config, name, template):
        Writer.__init__(self)
        self.config = config
        self.name = name
        self.template = template

    # Translation
    def translate(self):
        translator = LaTeXTranslator(
                self.document, self.config,
                self.name, self.template)
        self.document.walkabout(translator)
        self.output = translator.astext()


##############################
# LaTeX Translator
class LaTeXTranslator(NodeVisitor):

    def __init__(self, document, config, name, template):
        NodeVisitor.__init__(self, document)
        self.config = config
        self.name = name
        self.template = template
        self.body = []
        self.title = ''

        self.sections = [
                'part', 'chapter', 'section', 'subsection',
                'subsubsection', 'paragraph', 'subparagraph']

        level = -2
        if self.name == 'bacch':
            if not self.config.bacch_use_parts:
                level = -1
        elif self.name == 'gnomon':
            level = 0

        self.level_sect = self.level_start = level

        self.open_paragraph = False

        # Configure Nodes
        for (name, job) in active_nodes:
            if job == 'skip':
                setattr(self, 'visit_%s' % name, skip_node)
            elif job == 'pass':
                setattr(self, 'visit_%s' % name, pass_node)
                setattr(self, 'depart_%s' % name, pass_node)
            else:
                raise ValueError("Node Handler Error: %s" % name)

    # Render Text
    def astext(self):
        text = ''.join(self.body)

        # Render Template
        if self.template is not None:
            (path, fname, dirname) = self.template 

            jenv = jinja.Environment(
                    loader=jinja.FileSystemLoader(dirname),
                    block_start_string='\\BLOCK{',
                    block_end_string='}',
                    variable_start_string='\\VAR{',
                    variable_end_string='}',
                    comment_start_string='\\#{',
                    comment_end_string='}',
                    line_statement_prefix='%%',
                    line_comment_prefix='%#',
                    trim_blocks=True,
                    autoescape=False)
                    

            template = jenv.get_template(fname)

            text = template.render(
                    body=text,
                    title=self.title)

            #t = jinja2.escape(self.template) 
            #template = jinja2.Template(t) 
            #text = template.render(
            #    body=text,
            #    title=self.title)
        return text

    ###################
    # Structural Notes

    # Document
    def visit_document(self, node):
        pass
        
    def depart_document(self, node):
        pass

    # Sections
    def visit_section(self, node):

        # Fetch Title
        title = node.next_node().astext()

        # Increment Section Level
        self.level_sect += 1
        self.open_paragraph = True

        # Add Line
        if self.level_start == self.level_sect - 1:
            self.title = title


        elif self.level_sect > -1:

            section = self.sections[self.level_sect]
            number = '*'
            try:
                if getattr(self.config, '%s_numbers_%s' %
                           (self.name, section)):
                    number = ''
            except:
                if getattr(self.config, '%s_numbers' % self.name):
                    number = ''

            self.body.append('\n\\%s%s{%s}\n' % (section, number, title))

    def depart_section(self, node):

        # Decrement Section Level
        self.level_sect += -1

    # Paragraph
    def visit_paragraph(self, node):
        self.body.append('\n')

        if self.open_paragraph and getattr(
                self.config, '%s_noindent' % self.name):
            self.body.append('\n\\noindent')

    def depart_paragraph(self, node):
        self.body.append('\n')

    # Text
    def visit_Text(self, node):

        # Extract Text
        text = node.astext()

        if self.open_paragraph:
            self.open_paragraph = False

            if getattr(self.config, '%s_lettrine' % self.name):
                text = self.lettrine(text)

        self.body.append(text)

    def depart_Text(self, node):
        pass

    # Lettrine
    def lettrine(self, text):

        # Fetch Lettrine Config
        try:
            conf = getattr(self.config, '%s_lettrine_conf' % self.name)
            section = self.sections[self.level_sect]
            conf = conf[section]

            # Extract Config
            options = conf['options']
            leader = conf['leader']
            words = conf['letters']

        except:
            return text

        # Split Text
        base = text.split(' ')

        if not leader:
            base[0] = '\\lettrine[%s]{}{%s' % (options, base[0])
        else:
            word = base[0]
            length = len(word)

            # Separate Leader
            if word[0] == '"' or word[0] == "'":
                leader = word[0:1]
                if length > 2:
                    rest = word[2:]
                else:
                    rest = ''
            else:
                if length > 1:
                    leader = word[0]
                    rest = word[1:]
                else:
                    leader = word[0]
                    rest = ''

            # Write Lettrine
            base[0] = '\\lettrine[%s]{%s}{%s' % (options, leader, rest)

        # Close Lettrine
        if len(base) > words:
            base[words + 1] += '}'
        else:
            base[-1] += '}'

        return ' '.join(base)

    #####################
    # Block Markup

    #####################
    # Inline Markup

    # String
    def visit_strong(self, node):
        self.body.append('\\textbf{')

    def depart_strong(self, node):
        self.body.append('}')

    # Emphasis
    def visit_emphasis(self, node):
        self.body.append('\\emph{')

    def depart_emphasis(self, node):
        self.body.append('}')

    def visit_literal_inline(self, node):
        self.body.append('\\texsc{')

    def depart_literal_inline(self, node):
        self.body.append('}')


    def visit_literal_emphasis(self, node):
        self.body.append('\\texsc{')

    def depart_literal_emphasis(self, node):
        self.body.append('}')

    def visit_literal(self, node):
        self.body.append("Lit:")

    def depart_literal(self, node):
        self.body.append("}")
