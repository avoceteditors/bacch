# Module Imports
import re

#########################################
# Node Base Class
class Node():

    def __init__(self, element, base, ns):
        self.element = element
        self.base = base
        self.children = True
        self.alternate_parse = False
        self.ns = ns
    
    def altparse(self):
        return self.alternate_parse

    def read_children(self):
        return self.children

    def compile(self):
        pass

    def find_parent(self, element, search):
        for i in self.element.iterancestors(tag = search):
            print(i)

    def list_check(self):
        parent = self.element.getparent()
        book = self.ns['book']
        listitem = '{%s}listitem' % book

        if parent.tag == listitem:
            self.indent = '      '
        else:
            self.indent = None

    def fetch_title(self):
        
        self.title = self.element.xpath('book:title|book:info/book:title',
                namespaces = self.ns)[0].text

        self.idref = self.element.attrib['id']

        


##########################################
# Metadata Elements
class node_book_info(Node):
    
    def __init__(self, element, base, content):
        Node.__init__(self, element, base, content)
        self.children = False

class node_book_title(Node):

    def __init__(self, element, base, content):
        Node.__init__(self, element, base, content)
        self.children = False

##########################################
# Section Elements
class node_book_series(Node):
    pass

class node_book_book(Node):

    def compile(self):
        self.fetch_title()

class node_book_chapter(Node):
    
    def compile(self):
        self.fetch_title()

class node_book_section(Node):
    
    def compile(self):

        self.fetch_title()

##########################################
# Block Elements
class node_book_para(Node):
    
    def compile(self):
        self.list_check()



##########################################
# List Elements
class node_book_itemizedlist(Node):
    pass

class node_book_listitem(Node):
    pass


##########################################
# Program Elements
class node_book_programlisting(Node):
    pass

class node_book_userinput(Node):
    pass

class node_book_computeroutput(Node):
    pass

class node_book_prompt(Node):
    pass

class node_book_replaceable(Node):
    pass

##########################################
# Inline Elements
class node_book_code(Node):
    pass

class node_book_emphasis(Node):
    
    def compile(self):
        attr = self.element.attrib

        try:
            self.role = attr['role']
        except:
            self.role = 'em'
        
        

class node_book_link(Node):
    
    def compile(self):

        attr = self.element.attrib
        href = attr['{http://www.w3.org/1999/xlink}href']

        if self.element.text is None:
            self.element.text = href
