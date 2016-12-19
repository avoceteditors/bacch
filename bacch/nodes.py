import bacch

# Node Base Class
class Node():
    
    def __init__(self, element, datahandler):
        self.element = element
        self.datahandler = datahandler
        self.readchildren = True

    def compile(self):
        pass

    def section_compile(self):
        self.page = False
        attr = self.element.attrib
        try:
            check = attr['page']
            if check == 'yes':
                self.page = True
        except:
            pass

# Metadata Elements
class book_info(Node):
    def __init__(self, element, datahandler):
        Node.__init__(self, element, datahandler)
        self.readchildren = False

class book_title(Node):
    def __init__(self, element, datahandler):
        Node.__init__(self, element, datahandler)
        self.readchildren = False

class bacch_include(Node):
    def __init__(self, element, datahandler):
        Node.__init__(self, element, datahandler)
        self.readchildren = False



# Section Elements

class book_series(Node):

    def compile(self):
        self.section_compile()

class book_book(Node):
    
    def compile(self):
        self.section_compile()

class book_part(Node):
    def compile(self):
        self.section_compile()

class book_chapter(Node):
    def compile(self):
        self.section_compile()

class book_section(Node):

    def compile(self):
        self.section_compile()

# Block Elements
class book_para(Node):
    pass

class book_programlisting(Node):
    def __init__(self, element, datahandler):
        Node.__init__(self, element, datahandler)
        self.readchildren = False



# List Elements

class book_itemizedlist(Node):
    pass

class book_listitem(Node):
    pass


# Inline Elements
class book_emphasis(Node):
    pass

class book_code(Node):
    def __init__(self, element, datahandler):
        Node.__init__(self, element, datahandler)
        self.readchildren = False

# Link
class book_link(Node):   
    def __init__(self, element, datahandler):
        Node.__init__(self, element, datahandler)
        self.readchildren = True


