import bacch

class HTMLTranslator(bacch.Translator):

    def init_subclass(self):
        self.prefix = 'html'

    
    # Section Handlers
    def open_book_series(self, node):
        pass

    def close_book_series(self, node):
        pass

    def open_book_book(self, node):
        pass

    def close_book_book(self, node):
        pass

    def open_book_part(self, node):
        pass

    def close_book_part(self, node):
        pass

    def open_book_chapter(self, node):
        pass

    def close_book_chapter(self, node):
        pass

    def open_book_section(self, node):
        pass

    def close_book_section(self, node):
        pass


    # Block Handlers
    def open_book_para(self, node):
        pass

    def close_book_para(self, node):
        pass


    # List Handlers
    def open_book_itemizedlist(self, node):
        pass

    def close_book_itemizedlist(self, node):
        pass

    def open_book_listitem(self, node):
        pass

    def close_book_listitem(self, node):
        pass



