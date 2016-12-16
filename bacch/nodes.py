import bacch

# Node Base Class
class Node():
    
    def __init__(self, element, datahandler):
        self.element = element
        self.datahandler = datahandler
        self.readchildren = True

    def compile(self):
        bacch.log.warn("%s Node Handler not ready" % self.element.tag)

# Metadata Elements
class book_info(Node):
    def __init__(self, element, datahandler):
        Node.__init__(self, element, datahandler)
        self.readchildren = False

class book_title(Node):
    def __init__(self, element, datahandler):
        Node.__init__(self, element, datahandler)
        self.readchildren = False


# Section Elements

class book_series(Node):
    pass

class book_book(Node):
    pass

class book_part(Node):
    pass

class book_chapter(Node):
    pass

class book_section(Node):
    pass


# Block Elements
class book_para(Node):
    pass


# List Elements

class book_itemizedlist(Node):
    pass

class book_listitem(Node):
    pass
