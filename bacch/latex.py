from bacch.translator import BaseTranslator
import re


class Translator(BaseTranslator):

    extension = 'tex'

    ##############################
    # LaTex Reserve Characters
    def clean_latex(self, text):
        print('test')

        # Figure out reserve characters

        return text

    ##############################
    # Document
    def start_document(self):

        options = ['openright', 'pdflatex', '10pt']
        docclass = '\\documentclass[%s]{book}\n' % ','.join(options)

        packages = self.set_packages()

        header = [docclass, packages, '\\begin{document}\n']
        return '\n'.join(header)

    def end_document(self):
        return '\n\\end{document}'

    def set_packages(self):

        packages = {
            'listings': None,
            'scrextend': None,
            'mdframed': ['framemethod=default'],
            'framed': None,
            'xcolor': None,
            'titlesec': ['explicit', 'noindentafter'],
            'fancyhdr': None,
            'setspace': None,
            'titletoc': None,
            'microtype': ['tracking'],
            'inputenc': ['utf8'],
            'bookmark': None,
            'lettrine': None,
            'geometry': None,
            'textcase': None,
            'babel': ['english'],
            'pifont': None
        }

        books = ['series', 'book']
        if self.build_type['element'] in books:
            packages['geometry'] = ['b5paper']
        else:
            packages['geometry'] = ['letterpaper']

        usepackage = []
        for i in packages:
            if packages[i] is None:
                pack = '\\usepackage{%s}' % i
            else:
                opts = ','.join(packages[i])
                pack = '\\usepackage[%s]{%s}' % (opts, i)
            usepackage.append(pack)

        # Additional Commands
        usepackage.append('\n')

        commands = [
            '\\frenchspacing',
            '\\definecolor{shadecolor}{rgb}{1,0,0}',
            '\\mdfsetup{backgroundcolor=gray}',
            '\\newmdenv{code}'
            ]

        for c in commands:
            usepackage.append(c)

        return '\n'.join(usepackage)

    ##############################
    # Section Parsers

    # Series
    def start_book_series(self, node):
        pass

    def end_book_series(self, node):
        pass

    # Book
    def start_book_book(self, node):
        pass

    def end_book_book(self, node):
        pass

    def start_book_part(self, node):
        title = node.title

        base = ['\\part*{%s}\n' % title]

        return ''.join(base)

    def end_book_part(self, node):
        pass

    def start_book_chapter(self, node):
        title = node.title

        base = ['\\chapter*{%s}\n' % title]

        return ''.join(base)

    def end_book_chapter(self, node):
        pass

    # Section
    def start_book_section(self, node):

        title = node.title

        base = ['\\section*{%s}\n' % title]

        return ''.join(base)

    def end_book_section(self, node):
        pass

    ################################
    # Block Elements

    # Paragraph
    def start_book_para(self, node):

        listitem = '{%s}listitem' % node.ns['book']
        parent = node.element.getparent()

        if parent.tag == listitem:
            index = parent.index(node.element)
            
            if index > 0:
                return '\n      '
            else:
                ' '
        else:
            return '\n'

    def end_book_para(self, node):
        return '\n'

    ################################
    # List Elements

    # itemizedlist
    def start_book_itemizedlist(self, node):
        return '\n\\begin{itemize}\n'

    def end_book_itemizedlist(self, node):
        return '\n\\end{itemize}\n'

    # listitem
    def start_book_listitem(self, node):
        return '\\item '

    def end_book_listitem(self, node):
        return '\n'

    # programlisting
    def start_book_programlisting(self, node):

        base = ['\n\\begin{framed}']

        return ''.join(base)

    def end_book_programlisting(self, node):
        return '\n\\end{framed}\n'

    # userinput
    def start_book_userinput(self, node):
        pass

    def end_book_userinput(self, node):
        pass

    # computeroutput
    def start_book_computeroutput(self, node):
        pass

    def end_book_computeroutput(self, node):
        pass

    # replaceable
    def start_book_replaceable(self, node):
        return '\\emph{'

    def end_book_replaceable(self, node):
        return '}'

    # prompt
    def start_book_prompt(self, node):
        pass

    def end_book_prompt(self, node):
        pass

    #####################################
    # Inline Elements

    # code
    def start_book_code(self, node):
        pass

    def end_book_code(self, node):
        pass

    # emphasis
    def start_book_emphasis(self, node):

        if node.role == 'em':
            return '\\emph{'
        elif node.role == 'strong':
            return '\\textbf{'

    def end_book_emphasis(self, node):
        return '}'

    # link
    def start_book_link(self, node):
        pass

    def end_book_link(self, node):
        pass
