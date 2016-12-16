# Module Imports
import bacch



class BaseBuilder():

    def __init__(self, build, datahandler):
        self.build = build
        self.datahandler = datahandler
        self.project = datahandler.fetch()

        # Run Subclass Methods
        self.init_subclass()


    def compile(self, doctree):
        elements = doctree.getchildren()
        ns = bacch.__xmlns__['bacch']
    
        for element in elements:
            
            if element.tag == '{%s}include' % ns:
                href = element.attrib['href']

                try:
                    basetree = self.project[href].fetch()
                    newtree = self.compile(basetree)
                    newtree.set('{%s}inc' % ns, "yes")
                    doctree.replace(element, newtree)
                except:
                    bacch.log.warn("Bad Include: %s" % href)
            else:
                self.compile(element)
        return doctree


class PageBuilder(BaseBuilder):

    def init_subclass(self):
        element = self.build['element']
        elements = []
        if element == '*':
            for page in self.project:
                e = self.project[page].fetch()
                elements.append(e)
        else:
            target = self.build['target']
            e = self.project[target].fetch()
            elements = [e] 
            

        self.elements = elements
    
            


class BookBuilder(BaseBuilder):

    def init_subclass(self):

        # Compile Doctrees
        for page in self.project:
            element = self.project[page].fetch()
            self.compile(element)

        content = bacch.fetch_element(self.datahandler.master,
                '/bacch:project/bacch:content')[0]
        content = self.compile(content)

        self.elements = bacch.fetch_element(content, '//book:%s' % build['element'])

