import bacch

class HTMLTranslator(bacch.Translator):

    def init_subclass(self):
        self.prefix = 'html'

    # Document
    def open_document(self):
        header = ["<html>", "<head>"]

        close_head = ['</head>', '<body>']
        for i in close_head:
            header.append(i)

        return '\n'.join(header)

    def close_document(self):
        footer = ['</body>', '</hmtl>']
        return '\n'.join(footer)
    
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

    def open_book_programlisting(self, node):
        pass

    def close_book_programlisting(self, node):
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


    # Inline Handlers
    def open_book_link(self, node):
        pass

    def close_book_link(self, node):
        pass

    def open_book_emphasis(self, node):
        pass

    def close_book_emphasis(self, node):
        pass

    def open_book_code(self, node):
        pass

    def close_book_code(self, node):
        pass


