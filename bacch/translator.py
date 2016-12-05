import lxml.etree as ET
import bacch.node
import re

class BaseTranslator():


    def init(self, config, data, doctree, build_type):
        self.config = config
        self.data = data
        self.doctree = doctree
        self.text = []
        self.meta = {}
        self.build_type = build_type

    # Walk through Doctree
    def walkthrough(self):

        self.ns = self.config['ns']

        self.rns = {}
        for key in self.ns:
            value = self.ns[key]
            self.rns[value] = key

        # Walk Text
        self.walk(self.doctree)

    # Fetch Text
    def fetch(self):
        
        header = self.start_document()
        text = ''.join(self.text)
        footer = self.end_document()
        return '\n\n'.join([header, text, footer])
       
    def start_document(self):
        pass
    def end_document(self):
        pass

    def walk(self, base, main = None):


        for element in base.iterchildren():
            try:
                if isinstance(element, ET._Comment):
                    pass
                else:
                    (name, tag, ns) = self.getns(element)
                    node = getattr(bacch.node, 'node_%s_%s' % (name, tag))
                    node = node(element, base, self.ns)

                    if node.read_children():
                        element_text = []
                        setattr(node, 'build', self.build_type)
                      
                        # Compile Node
                        node.compile()

                        # Configure Node Handlers
                        starttag = getattr(self, 'start_%s_%s' % (name, tag))
                        endtag = getattr(self, 'end_%s_%s' % (name, tag))

                        start = starttag(node)
                        end = endtag(node)

                        # Start Tag
                        self.add(start, True)

                        # Add Text
                        if name == 'latex':
                            reserve_chars = '[{}\\\^&\%\$#~_]'
                            text = self.latex_escape(
                                    element.text, reserve_chars)
                        else:
                            text = element.text

                        self.add(text)

                        # Subparse
                        self.walk(element, base)

                        # End Tag
                        self.add(end, True)

                        # Add Tail
                        if name == 'latex':
                            reserve_chars = '[{}\\\^&\%\$#~_]'
                            text = self.latex_escape(
                                    element.tail, reserve_chars)
                        else:
                            text = element.tail
                        self.add(element.tail)





            except:
                msg = "Error: Unable to parse %s" % element.tag
                print(msg)

    def latex_escape(self, text, reserve_chars):
        text = re.sub(
                reserve_chars,
                self.latex_escape_match,
                text)
        return text

    def latex_escape_match(self, match):
        if match.group(0) == '~':
            return '$\\sim$'
        elif match.group(0) == '\\':
            return '$\\backslash$'

        elif match.group(0) == '^':
            return '$\\^{}'

    def add(self, text, preserve = False):

        if text is not None and isinstance(text, str):
            if preserve:
                self.text.append(text)
            elif not re.match('^[\s]*$', text):
                self.text.append(text)

    def getns(self, element):

        tag = re.sub('^{.*?}','', element.tag)
        ns = re.sub('}.*$', '', element.tag)[1:]
        try:
            name = self.rns[ns]
        except:
            raise ValueError("Invalid namespace: %s" % ns)

        return name, tag, ns

    def parse_meta(self, element):

        return {}

