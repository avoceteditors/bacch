# Module Imports
import lxml.etree as ET
import os, os.path

# Entry Class
class Entry():
    """ Handler for file-level XML reads.  Provides methods
    in preparing and organizing the data during the read to
    save on performance later.
    """

    # Initialize Class
    def __init__(self, args, sourcedir, config, filename, name):
        self.path = os.path.join(sourcedir, filename)
        self.config = config
        self.args = args
        self.mtime = os.path.getmtime(self.path)

        self.sects = {}

    # Check Status of Read
    def check_status(self):
        """ Method checks whether the file has been updated
        since it was last read.  In the event that it has
        been updated, it reloads the XML.
        """
        newmtime = os.path.getmtime(self.path)

        if newmtime > self.mtime or self.args.sync:
            self.update()
    
    # Update XML Read
    def update(self):
        """ Method reads the XML from file.
        """

        # Open File
        f = open(self.path, 'rb')
        content = f.read()
        f.close()

        try:
            self.doctree = ET.fromstring(content)
        except:
            self.doctree = ET._Element
            print("XMLError: Unable to parse %s" % self.path)

        # Load Section Data
        self.load_sections()

    # Retrieve Sections
    def fetch_sections(self):
        """ Returns the section data, including idrefs,
        titles and abstract text for links.
        """

        return self.sects

    # Load Sections
    def load_sections(self):
        """ Reads section data from the XML doctree, finding
        each book, chapter and section from the file and
        saves the idrefs, titles and abstracts.
        """

        matches = ['series', 'book', 'part', 'chapter', 
                'section']
        match = '|//book:'
        base = '//book:' + match.join(matches)

        sects = {}
        sections = self.doctree.xpath(base,
                namespaces = self.config['ns'])
        
        for sect in sections:
            idref = sect.attrib['id']
            
            title = sect.xpath('book:title|book:info/book:title',
                    namespaces = self.config['ns'])[0]

            if title is not None:
                title = title.text

            abstract = sect.xpath('book:info/book:abstract',
                    namespaces = self.config['ns'])

            sects[idref] = {
                    'title': title 
                    }

        self.sects = sects
            

