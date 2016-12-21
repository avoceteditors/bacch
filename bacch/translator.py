import lxml
import re

import bacch

class Translator():

    def __init__(self, build, elements, datahandler):
        self.build = build
        self.body = None
        self.text = {}
        self.name = ''
        self.elements = elements
        self.datahandler = datahandler

        self.init_subclass()

    def fetch(self):
        ret_text = []
        for key in self.text:
            body = ''.join(self.text[key])
            head = self.open_document()
            foot = self.close_document()
            newtext = '\n\n'.join([head, body, foot])

            self.text[key] = newtext

        return self.text

    def walkthrough(self):
        
        for element in self.elements:
            if self.body is not None:
                self.text[self.name] = self.body
            self.name = element.attrib['id']
            self.body = []
            self.walk(element)

    def walk(self, elements):

        for element in elements:
            if not isinstance( element, lxml.etree._Comment):
           
                (name, tag, ns) = self.fetch_id(element)

                if name is not None:
                    try:
                        node = getattr(bacch.nodes, '%s_%s' % (name, tag))
                        node = node(element, self.datahandler)

                        if node.readchildren:
                            node_start = self.fetch_handler(self, 
                                'open_%s_%s' % (name, tag))
                            node_end = self.fetch_handler(self, 
                                'close_%s_%s' % (name, tag))
                            self.crawl(node, element, node_start, node_end)

                    except:
                        bacch.log.warn("Node Handler: %s"  % tag)

    def crawl(self, node, element, start, end):
        if start and end:

            # Walk Elements
            self.walk(element)


                    
    def fetch_handler(self, obj, name):
        try: 
            return getattr(obj, name)
        except:
            bacch.log.warn("%s needs handler: %s" % (obj, name))
            return False

    def fetch_id(self, element):
        tag = re.sub('^{.*?}', '', element.tag)
        ns = re.sub('}.*$', '', element.tag[1:])

        try:
            name = bacch.__rxmlns__[ns]
        except:
            bacch.log.warn("Invalid Namespace %s at: %s" % (ns, element.tag))
            name = None

        return name, tag, ns
