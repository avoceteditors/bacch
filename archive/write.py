# Copyright (c) 2018, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
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

from docutils import nodes, writers
from sphinx.writers.latex import LaTeXWriter 
import re
import jinja2
import os.path

from logging import getLogger
logger = getLogger()



class BacchLaTeXWriter(LaTeXWriter):

    settings_spec = ('No options here.', '',())
    settings_defaults = {}

    output = None 

    def __init__(self, builder):
        writers.Writer.__init__(self)
        self.builder = builder
        self.template_path = None
        self.title = ""

    def set_template(self, path, title):
        self.template_path = path
        self.title = title

    def translate(self):
        visitor = BacchLaTeXTranslator(self.document, self.builder.config)
        self.document.walkabout(visitor)
        text = visitor.astext()

        # Apply Template
        if self.template_path is not None:
            path = self.template_path[0]
            filename = self.template_path[1]

            latex_env = jinja2.Environment(
                block_start_string = '\%s{' % self.builder.config.bacch_latex_block,
	        block_end_string = '}',
	        variable_start_string = '\%s{' % self.builder.config.bacch_latex_var,
	        variable_end_string = '}',
	        comment_start_string = '\#{',
	        comment_end_string = '}',
	        line_statement_prefix = '%%',
	        line_comment_prefix = '%#',
	        trim_blocks = True,
	        autoescape = False,
    	        loader = jinja2.FileSystemLoader(path)
            )
            template = latex_env.get_template(filename)
            try:
                self.output = template.render(body=text, title=self.title)
            except:
                logger.warn("\nError Rendering Template")
                self.output = text
        else:
            logger.warn("\nNo template found")
            self.output = text 

class BacchLaTeXTranslator(nodes.NodeVisitor):
    latex_substitution = [
        ("\\\\", "\\textbackslash{}"),
        ("\{", "\\{"),
        ("\}", "\\}"),
        ("\$", "\\$"),
        ("\&", "\\&"),
        ("\#", "\\#"),
        ("\^", "\\textasciicircum{}"),
        ("_", "\\_"),
        ("\~", "\\textasciitilde{}"),
        ("%", "\\%"),
        ("\<", "\\textless{}"),
        ("\>", "\\textgreater{}"),
        ("\|", "\\textbar{}")
    ]

    skip_nodes = [
        'title'
    ]
    def __init__(self, document, config):
        nodes.NodeVisitor.__init__(self, document)
        self.config = config 

        self.body = []

        # Set Levels
        self.level = -2 
        self.levels = ['chapter', 'section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']
        if self.config.bacch_use_parts:
            self.levels = ['part'] + self.levels

        self.open_paragraph = False

        for node in self.skip_nodes:
            setattr(self, "visit_%s" % node, self.skip_node)

    def skip_node(self, node):
        raise nodes.SkipNode

    def astext(self):
        return ''.join(self.body)

    def append(self, text):
        self.body.append(text)

    def visit_start_of_file(self, node):
        pass
    def depart_start_of_file(self, node):
        pass

    def visit_document(self, node):
        pass

    def depart_document(self, node):
        pass

    def visit_highlightlang(self, node):
        pass
    def depart_highlightlang(self, node):
        pass

    def visit_section(self, node):
        title = node.next_node().astext()
        self.level += 1
        
        try:
            level = self.levels[self.level]
            if not self.level < 0:
                header_line = '\n\\%s*{%s}\n' % (
                    level, title)
            else:
                header_line = ""
        except:
            header_line = "\n\\textbf{%s}\n" % title

        self.append(header_line)

        # Housekeeping
        self.open_paragraph = True

    def depart_section(self, node):
        self.level += -1

    def visit_rubric(self, node):
        self.open_paragraph = False
        self.open_rubric = True
        self.append("\\textbf{")

    def depart_rebruic(self, node):
        self.open_rubric = False
        self.append("}")

    def visit_paragraph(self, node):
        self.append("\n")
        
        if self.open_paragraph and self.config.bacch_noindent:
            self.open_paragraph = False
            self.append("\n\\noindent")
            

    def depart_paragraph(self, node):
        self.append('\n')

    def visit_Text(self, node):

        text = node.astext()

        # Escape Latex
        for (match, replace) in self.latex_substitution:
            if re.match("^.*?%s" % match, text):
                text = re.sub(match, replace, text)

        self.append(text)

    def depart_Text(self, node):
        pass

    def visit_strong(self, node):
        self.append("\\textbf{")

    def depart_strong(self, node):
        self.append("}")

    def visit_emphasis(self, node):
        self.append("\\emph{")
    def depart_emphasis(self, node):
        self.append("}")


    def visit_compound(self, node):
        pass

    def depart_compound(self, node):
        pass

    # Code Blocks
    def visit_literal_block(self, node):
        self.append("\n\\begin{lstlisting}\n")

    def depart_literal_block(self, node):
        self.append("\n\\end{lstlisting}\n")

    # Lists

    def visit_list_item(self, node):
        self.append('\n\\item ')
    def depart_list_item(self, node):
        self.append('\n\n')

    def visit_bullet_list(self, node):
        self.append('\n\\begin{itemize}\n')

    def depart_bullet_list(self, node):
        self.append('\n\\end{itemize}\n')


