import re
from docutils import nodes
from docutils.nodes import NodeVisitor
from sphinx.writers.latex import LaTeXTranslator

from ..log import BacchLogger



class BacchLaTeXTranslator(NodeVisitor, BacchLogger):

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

    def __init__(self, document, builder):
        NodeVisitor.__init__(self, document)
        self.init_logger()
        self.body = []
        self.config = builder.config
        self.builder = builder

    # Helper Methods
    def astext(self):
        return ''.join(self.body) 

    def skip_node(self, node):
        raise nodes.SkipNode

    def add(self, text):
        self.body.append(text)


    # Structural Elements
    def visit_document(self, node):
        pass

    def depart_document(self, node):
        pass


    def visit_section(self, node):
        pass

    def depart_section(self, node):
        pass

    def visit_paragraph(self, node):
        self.add("\n")

    def depart_paragraph(self, node):
        self.add("\n")

    def visit_Text(self, node):
        text = node.astext()

        # Word Counter?

        # Sanitize for LaTeX
        for (match, replace) in self.latex_substitution:
            if re.match("^.*?%s" % match, text):
                text = re.sub(match, replace, text)

        self.add(text)

    def depart_Text(self, node):
        pass

    # Block Elements
    def visit_title(self, node):
        self.skip_node(node)

    def depart_title(self, node):
        pass

    # Inline ELemnts
    def visit_strong(self, node):
        self.add("\\textbf{")

    def depart_strong(self, node):
        self.add("}")

    def visit_emphasis(self, node):
        self.add("\\textit{")

    def depart_emphasis(self, node):
        self.add("}")




