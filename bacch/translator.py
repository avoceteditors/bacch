import lxml
import re

import bacch

class Translator():

    def __init__(self, build, build_type, elements, datahandler):
        self.build = build
        self.build['type'] = build_type        
        self.elements = elements
        self.datahandler = datahandler

        self.init_subclass()

        for element in self.elements:
            element.attrib['page'] = 'yes'
    

    def walkthrough(self):
        self.body = []
        self.walk(self.elements)
        #print(self.body)

    def walk(self, elements):

        for element in elements:
            if not isinstance( element, lxml.etree._Comment):
           
                (name, tag, ns) = self.fetch_id(element)

                if name is not None:
                    try:
                        node = getattr(bacch.nodes, '%s_%s' % (name, tag))
                        node = node(element, self.datahandler)

                        node.compile()

                        if node.readchildren:
                            node_start = self.fetch_handler(self, 
                                'open_%s_%s' % (name, tag))
                            node_end = self.fetch_handler(self, 
                                'close_%s_%s' % (name, tag))
                            self.crawl(node, element, node_start, node_end)

                    except:
                        bacch.log.warn("Node Handler: bacch.nodes.%s_%s"  % (name, tag))
                        print(element.attrib)

    def crawl(self, node, element, start, end):
        if start and end:
            
            # Text
            self.add(element.text)            

            # Walk Elements
            self.walk(element)

            # Tail
            self.add(element.tail)


    def add(self, text):
        if not re.match('^[\s]*$', text):
            text = re.sub('\n', '', text)
            self.body.append(text)
                    
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
