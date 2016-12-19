import bacch

class HTMLTranslator(bacch.Translator):

    def init_subclass(self):
        self.prefix = 'html'

    # Page
    def open_page(self, node):
        header = ["<html>", "<head>"]

        header.append('</head>')
        header.append('<body>')

        return '\n'.join(header)

    def close_page(self, node):
        footer = ['</body>', '</html>']
        return '\n'.join(footer)
   
    # Section Handlers
    def open_book_series(self, node):
        if node.page:
            text = self.open_page(node)
            self.body.append(text)
        else:
            pass

    def close_book_series(self, node):
        if node.page:
            text = self.close_page(node)
            self.body.append(text)
        else:
            pass

    def open_book_book(self, node):
        pass
        if node.page:
            text = self.open_page(node)
            self.body.append(text)
        else:
            pass

    def close_book_book(self, node):
        if node.page:
            text = self.close_page(node)
            self.body.append(text)
        else:
            pass

    def open_book_part(self, node):
        if node.page:
            text = self.open_page(node)
            self.body.append(text)
        else:
            pass

    def close_book_part(self, node):
        if node.page:
            text = self.close_page(node)
            self.body.append(text)
        else:
            pass

    def open_book_chapter(self, node):
        if node.page:
            text = self.open_page(node)
            self.body.append(text)
        else:
            pass

    def close_book_chapter(self, node):
        if node.page:
            text = self.close_page(node)
            self.body.append(text)
        else:
            pass    

    def open_book_section(self, node):
        if node.page:
            text = self.open_page(node)
            self.body.append(text)
        else:
            pass

    def close_book_section(self, node):
        if node.page:
            text = self.close_page(node)
            self.body.append(text)
        else:
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


    # Inline Elements
    def open_book_emphasis(self, node):
        pass

    def close_book_emphasis(self, node):
        pass

    # Links
    def open_book_link(self, node):
        pass

    def close_book_link(self, node):
        pass    
