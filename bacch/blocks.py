

class Block():

    def __init__(self, content):
        self.name = content.tag
        self.attrib = content.attrib
        self.text = content.text

    def parse_latex(self):
        pass

    def parse_html(self):
        pass


class Paragraph(Block):
    pass
