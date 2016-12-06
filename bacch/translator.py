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

    def walk(self, base, main=None):
        build_format = self.build_type['format']
        for element in base.iterchildren():
            try:
                if isinstance(element, ET._Comment):
                    pass
                else:
                    (name, tag, ns) = self.getns(element)
                    node = getattr(bacch.node, 'node_%s_%s' % (name, tag))
                    node = node(element, base, self.ns)

                    if node.read_children():
                        setattr(node, 'build', self.build_type)

                        # Compile Node
                        node.compile()

                        # Configure Node Handlers
                        starttag = getattr(self, 'start_%s_%s' % (name, tag))
                        endtag = getattr(self, 'end_%s_%s' % (name, tag))

                        start = starttag(node)
                        end = endtag(node)

                        # Start Tag
                        self.add(start)

                        # Add Text
                        text = self.clean(element.text, build_format)

                        self.add(text)

                        # Subparse
                        self.walk(element, base)

                        # End Tag
                        self.add(end)

                        # Add Tail
                        text = self.clean(element.tail, build_format)
                        self.add(text)

            except:
                msg = "Error: Unable to parse %s" % element.tag
                print(msg)

    def clean(self, text, name):
        meth = getattr(self, 'clean_%s' % name)
        text = self.clean_latex(text)
        print('stuff')
        return text

    def add(self, text):

        if text is not None and not re.match('^[\s]*$', text):
            self.text.append(text)

    def getns(self, element):

        tag = re.sub('^{.*?}', '', element.tag)
        ns = re.sub('}.*$', '', element.tag)[1:]
        try:
            name = self.rns[ns]
        except:
            raise ValueError("Invalid namespace: %s" % ns)

        return name, tag, ns

    def parse_meta(self, element):

        return {}
