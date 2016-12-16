# Module Imports
import os.path
import re
import bacch

class DataEntry():

    def __init__(self, name, path, doctree):
        self.name = name
        self.path = path
        self.doctree = doctree

        # Set MTime
        self.mtime = os.path.getmtime(self.path)

        # Set Sections
        self.set_sects()

        # Log Stats
        self.set_stats()

    # Check MTime
    def check_mtime(self):
        newmtime = os.path.getmtime(self.path)
        return newmtime > self.mtime

    #############################
    # Set Idrefs
    def set_sects(self):
        base_elements = ['series', 'book', 'part', 'chapter', 'section']
        elements = '//book:%s' % '|//book:'.join(base_elements)
        self.sections = {}

        sects = bacch.fetch_element(self.doctree, elements)
        for sect in sects:
            idref = sect.attrib['id']
            title = bacch.fetch_element(sect, 'book:title|book:info/book:title')[0]
            title_text = title.text

            try:
                title_format = title.attrib['{%s}format' % bacch.__xmlns__['bacch']]
            except:
                title_format = None

            
            self.sections[idref] = {
                'title': title_text,
                'title_format': title_format}

    # Fetch Idrefs
    def fetch_sects(self):
        return self.sections

    
    #############################
    # Set Stats
    def set_stats(self):
        elements = bacch.fetch_element(self.doctree, '//book:para')

        lines = len(elements)
        base_text = self.find_text(elements)
        base = re.split('\s', base_text)
        text = []
        for i in base:
            if i != '':

                # Note: Add Spellcheck functionality here

                text.append(i)
        words = len(text)
        chars = len(''.join(text))

        self.stats = {
            "lines": lines,
            "words": words,
            "chars": chars
        }

    def find_text(self, elements):
        body = []
        for element in elements:
            for text in [element.text, self.find_text(element), element.tail]:
                if text is not None:
                    body.append(text)

        return ' '.join(body)

    def fetch_stats(self):
        return self.stats
