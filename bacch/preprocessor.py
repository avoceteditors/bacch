""" This module provides the Preprocessor class.  """

# Module Import
import bacch
import re
import lxml.etree

#######################################
# Preprocessor
class Preprocessor():

    """ This class provides preprocessing in rendering output.
    The preprocessor handles all common operations for all builds
    before the nodes are passed to the main processor, such as
    handling includes and link text."""

    # Initialize Class
    def __init__(self, build, reader):
        """ This method initializes the class and call all relevant
        methods used in preprocessing the document."""

        self.build = build
        self.reader = reader
        self.current_resource = ''
       
        # Fetch Doctree 
        self.data = reader.fetch()
        self.sect_data = reader.fetch_sects()

        # Iterate over Resources
        for resource in self.data:
            
            kind = self.reader.resources[resource]['type']
            if kind in ['source', 'blocks']:
                self.current_resource = kind

                for name in self.data[kind]:
                    entry = self.data[kind][name]
                    self.doctree = entry.fetch()

                    self.walk(self.doctree)

    # Walk Operation
    def walk(self, doctree): 
        """ This method walks through each element in the given
        doctree.  For each element, it attempts to call the element
        name as a method.  If the call fails, it calls walk() on the
        new element.  When the call passes, it passes the elment to
        that method.
        """

        for element in doctree:
            try:

                base = element.tag.split('}')             
                ns = bacch.__rxmlns__[base[0][1:]]
                tag = '%s_%s' % (ns, base[1])

                meth = getattr(self, tag)
                meth(element)
            except:
                self.walk(element)

    # Include Processing
    def bacch_include(self, element):
        """ This method handles <bacch:include/> elements,
        pull doctrees reads from self.data and adding them
        to the current doctree. """

        attr = element.attrib
        href = attr['href']
        if 'resource' not in attr:
            resource = self.current_resource
        else:
            resource = attr['resource']

        newdoctree = self.data[resource][href].fetch()
        self.doctree.replace(element, newdoctree)

        self.walk(newdoctree)


    # Link Processing
    def book_link(self, element):
        """ This method handles <book:link/> instances,
        writing in preliminary attributes required for later
        parsing."""

        attr = element.attrib
        
        # Find Resource
        if element.text is None:

            # Find href
            href = attr['href']
            
            if re.match('^http://|^https://', href):
                element.text = href
                bacch.__log__.debug('Setting link text to %s, title lookups not yet available.' % href)
            else:
                
                # Find Resource
                try:
                    resource = attr['resource']
                except:
                    resource = self.current_resource

                # Find Element
                try:
                    entry = self.sect_data[resource][href]
                    
                    # Set Text
                    element.text = entry['title']
                    
                    # Set Resource
                    element.set('resource', resource)

                    # Set Base Href
                    element.set('base_href', entry['href']) 

                    # Set idref
                    element.set('base_idref', href)

                except:
                    print("Exception: %s" % href)
