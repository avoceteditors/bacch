"""
This module provides the DataEntry class, which Bacch uses to
handle initial and first stage XML processing.  
"""
# Module Imports
import os, os.path
import re
import bacch

# Data Entry Class
class DataEntry():

    """ This class handles XML data from file-reads.

    In addition to storing the doctree for later reference,
    it also performs the initial file-level parsing of the data.
    Anything internal and specific to the local doctree is handled
    at this point, preparing the data it will need to pass to the
    processors at later stages and logging statistical information
    for separate reference."""

    # Initialize Class
    def __init__(self, name, path, doctree):
        """ This method initializes the class.  It takes a name
        value, a path and an lxml doctree as arguments and controls
        the initial data processing."""
        self.name = name
        self.path = path
        self.doctree = doctree

        # Set Mtime
        self.mtime = os.path.getmtime(self.path)

        # Set Section Data
        self.set_sects()

        # Gather Statistical Data
        self.set_stats()

    # Check File Mtime
    def check_mtime(self):
        """ This method tests the mtime on the given file and
        whether this time is more recent than the mtime it 
        recorded when the file was previous read.  It returns
        true if the current file is newer."""
        newmtime = os.path.getmtime(self.path)
        return newmtime > self.mtime

    # Fetch Doctree
    def fetch(self):
        """ This method fetches the lxml doctree for processing,
        by other modules."""
        return self.doctree

    # Set Section Data
    def set_sects(self):
        """ This method extracts sectional data from the doctree.

        When Bacch parses links, it can write in arbitrary text for
        the link name and hover text.  Rather than gathering this
        data on every run, it collect it on the file read and saves
        it for the processing modules in self.sections."""
        
        base_elements = ['series', 'book', 'part', 'chapter', 'section']
        elements = '//book:%s' % '|//book:'.join(base_elements)
        self.sections = {}

        sects = bacch.fetch_element(self.doctree, elements)
        for sect in sects:

            # Set Name 
            name = sect.attrib['id']
            
            # Set Title
            title_element = bacch.fetch_element(sect,
                'book:title|book:info/book:title')[0]

            # Set Format
            bacch_ns = bacch.__xmlns__['bacch']
            try:
                title_format = title_element.attrib[
                '{%s}format' % bacch_ns]
            except:
                title_format = None

            # Set Abstract
            base_abstract = bacch.fetch_element(sect,
                'book:info/book:abstract/book:para')
            if base_abstract == []:
                base_abstract = None

            self.sections[name] = {
                'title': title_element.text,
                'format': title_format,
                'base_abstract': base_abstract}

    # Fetch Sectional Data
    def fetch_sects(self):
        """ This method passes sectional data gathered from the
        doctree to the processing modules."""
        return self.sections

    # Gather Statistical Data
    def set_stats(self):
        elements = bacch.fetch_element(self.doctree, '//book:para')

        # Line Count
        line_count = len(elements)

        # Word List 
        self.text = []
        self.find_text(elements)
        text = ' '.join(self.text)        
        base_words = re.split('\W', text)
        words = [word for word in base_words if word != '']

        # Word Count
        word_count = len(words)

        # Character Count
        chars = 0
        for word in words:
            chars += len(word)
        self.stats = {
            "lc": line_count,
            "wc": word_count,
            "cc": chars,
            "words": words
        }

    # Fetch Stats
    def fetch_stats(self):
        return self.stats

    # Find Text in Doctree
    def find_text(self, elements):
        for element in elements:
            self.check_text(element.text)
            children = element.getchildren()
            if children != []:
                self.find_text(children)
            self.check_text(element.tail)

    # Test Text
    def check_text(self, text):
        if text is not None:
            self.text.append(text)
