# Module Imports
import lxml.etree as ET
import os, os.path

# Entry Class
class Entry():

    def __init__(self, args, sourcedir, config, filename, name):
        self.path = os.path.join(sourcedir, filename)
        self.config = config
        self.args = args
        self.mtime = os.path.getmtime(self.path)

        self.sects = {}

    def check_status(self):
        newmtime = os.path.getmtime(self.path)

        if newmtime > self.mtime or self.args.sync:
            self.update()

    def update(self):
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

    def fetch_sections(self):
        return self.sects

    def load_sections(self):
        matches = ['series', 'book', 'part', 'chapter', 'section']
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
            

