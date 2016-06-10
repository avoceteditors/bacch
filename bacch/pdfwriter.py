# Copyright (c) 2015, Kenneth P. J. Dyer
# All rights reserved.
#
# Redistribution and use in source and binary forms, 
# with or without modification, are permitted provided 
# that the following conditions are met:
#
# * Redistributions of source code must retain the 
#   above copyright notice, this list of conditions 
#   and the following disclaimer.
#
# * Redistributions in binary form must reproduce the 
#   above copyright notice, this list of conditions 
#   and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of bacch nor the names of its 
#   contributors may be used to endorse or promote 
#   products derived from this software without 
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS 
# AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED 
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING 
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN 
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Module Imports
import re
import os.path
import subprocess
import shutil
import xml.dom.minidom

from bacch import lib

# Writer Class for PDF
class PDFWriter():

    def __init__(self, args):
        self.args = args
        self.unit = args.book
        self.level = 0
        self.level_sect = 0
        self.body = []
        self.head = []
        self.text = {}
        self.info = {}
        self.config = {
            "font": "10pt"
                
                }
    ##########################################
    # Write Files
    def get_text(self):
        if self.args.verbose:
            lib.report("Writing LaTeX to file...")
        print(self.text)
        for key in self.text:
            if self.args.verbose:
                lib.report("Writing: %s" % key)

            content = ''.join(self.text[key])
            path = os.path.join(self.args.tmpdir, key)
            f = open(path, 'w')
            f.write(content)
            f.close()
            command = ['pdflatex', '--output-directory', 
                    self.args.tmpdir, path]
            subprocess.call(command)
            print(content)
    


    ###########################################
    # Process Text and Comments
    def visit_TEXT(self, node):
        text = self.parse_text(node)
        if text is not None:
            self.body.append(text)

    def parse_text(self, node):
        text = node.nodeValue
        if not re.match(r'^[ \t\n]*$', text):
            return text

    def depart_TEXT(self, node):
        pass

    def visit_COMMENT(self, node):
        return False

    def depart_COMMENT(self, node):
        pass


    #########################################
    # Special Handlers
    def visit_xi__include(self, node):
        return True

    def depart_xi__include(self, node):
        pass


    #########################################
    # Process Pages
    def visit_set(self, node):
        if self.args.single:
            self.getheader()
            self.body.append('\\begin{document}\n')
        return True

    def depart_set(self, node):
        if self.args.single:
            self.body.append('\\end{document}')
            self.text['master.tex'] = self.body

    def visit_book(self, node):
        self.level += 1
        title = self.gettitle(node)

        if self.args.single:
            self.body.append('\\part*{%s}\n' % title)

        elif self.unit == 'book':
            self.getheader()
            self.body.append('\\begin{document}\n')
            return True

    def depart_book(self, node):
        if self.args.single:
            pass
        elif self.unit == 'book':
           self.body.append('\\end{document\n}')

    def visit_part(self, node):
        self.level += 1
        title = self.gettitle(node)
        if self.args.single:
            self.body.append('\\chapter*{%s}\n' % title)
        elif self.unit == 'part':
            self.getheader()
            self.body.append('\\begin{document}\n')
        return True

    def depart_part(self, node):
        self.level += -1
        if self.args.single:
            pass
        elif self.unit == 'part':
            self.body.append('\\end{document}\n')

    def visit_chapter(self, node):
        self.level += 1
        title = self.gettitle(node)

        if self.args.single:
            self.body.append('\\section*{%s}\n' % title)
        elif self.unit == 'chapter':
            self.getheader()
            self.body = []
            self.body.append('\\begin{document}\n')
        return True

    def depart_chapter(self, node):
        self.level += -1
        if self.args.single:
            pass
        elif self.unit == 'chapter':
            self.body.append('\\end{document}')

    def visit_section(self, node):
        self.level += 1
        # Define Base Level for Sections
        if self.level_sect == 0:
            parent = node.parentNode.nodeName
            grand = node.parentNode.parentNode.nodeName
            if parent == 'chapter':
                self.level_sect = self.level
            elif parent == 'xi:include' and grand == 'chapter':
                self.level_sect = self.level

            # Index Unit
            if self.unit != "set":
                if self.unit == 'section':
                    self.level_sect += -1

        if self.unit == 'section':
            self.getheader()
            self.body.append('\\begin{document}\n')
        else:
            self.visit_sect(node)
        return True

    def depart_section(self, node):
        self.level += -1
        if self.unit == "section" and self.level_sect == self.level:
                self.body.append('\\end{document}')
        else:
            self.depart_sect(node)

    def visit_sect(self, node):
        title = self.gettitle(node)
        diff = self.level - self.level_sect
        if diff == 0:
            self.body.append('\\section*{%s}\n' % title)
        elif diff == 1:
            self.body.append('\\subsection*{%s}\n' % title)
        elif diff == 2:
            self.body.append('\\subsubsection*{%s}\n' % title)
        elif diff == 3:
            self.body.append('\\paragraph*{%s}\n' % title)
        else:
            self.body.append('\\subparagraph*{%s}\n' % title)

    def depart_sect(self, node):
        pass

    

    # Helper Methods
    def getheader(self):
        if self.head == []:
            prolog = [self.set_documentclass(), self.set_packages(),
                    self.set_titles, self.set_fancyheads]
            for i in prolog:
                if type(i) == str:
                    self.head.append(i)
        self.body = ['\n'.join(self.head)]


    def set_documentclass(self):
        options = ['openright']
        font = self.config['font']
        if font not in ['12pt', '10pt']:
            font = '10pt'
        options.append(font)

        opts = ','.join(options)
        return '\\documentclass[%s]{book}\n' % opts
        


    def set_packages(self):
        packages = {
            'titlesec':     ['explicit', 'noindentafter'],
            'fancyhdr':     None,
            'setspace':     None,
            'titletoc':     None,
            'framed':       None,
            'microtype':    ['tracking'],
            'inputenc':     ['utf8'],
            'bookmark':     None,
            'lettrine':     None,
            'geometry':     None,
            'textcase':     None,
            'babel':        ['english'],
            'pifont':       None
            }
        if self.args.single:
            packages['geometry'] = ['b5paper']

        pkgs = []
        for key in packages:
            if packages[key] is None:
                pkgs.append('\\usepackage{%s}\n' % key)
            else:
                options = ','.join(packages[key])
                pkgs.append('\\usepackage[%s]{%s}\n'
                        % (options, key))
        return ''.join(pkgs)



    def set_commands(self):
        return ''

    def set_titles(self):
        return ''

    def set_fancyheads(self):
        return ''

    def gettitle(self, node):
        title = ''
        for element in node.childNodes:
            if element.nodeName == 'title':
                title = self.fetch_text(element)
            elif element.nodeName == 'info':
                for el in element.childNodes:
                    if el.nodeName == 'title':
                        title = self.fetch_text(el)

        if title == '' or title is None:
            title = node.getAttribute('xml:id')

        return title

    def fetch_text(self, node):
        elements = node.childNodes
        for element in elements:
            return element.nodeValue

        
        
    # Fetch Content
    def fetch(self, node, check = None):
        if node is str:
            return node
        elif check is str:
            return check

        try:
            length = node.length
            if length == 1:
                check = self.fetch(node, check)
        except:
            for item in node.childNodes:
                try:
                    tag = item.tagname
                    if tag == 'info':
                        check = self.fetch(item, check)
                    elif tag == 'title':
                        check = self.fetch(item, check)
                except:
                    if str(type(item)) == "<class 'xml.dom.minidom.Text'>":
                        if not re.match(r'^[\S]*', item.nodeValue):
                            return item.nodeValue
                        else:
                            check = self.fetch(item, check)
        return check
            

    #########################################
    # Process Blocks
    def visit_info(self, node):
        parentname = node.parentNode.nodeName 
        if parentname == 'set':
            self.set_info(node, 'master')
        elif parentname == self.unit:
            self.set_info(node, 'unit')

        return False


    def set_info(self, node, unit):
        info = self.info
        info[unit] = {'authors': [], 'title': None}
        for i in node.childNodes:
            name = i.nodeName
            if name == 'title':
                info[unit]['title'] = self.fetch(i)
            elif name == 'author':
                self.set_author(i, unit)
            elif name == 'authorgroup':
                for person in i.childNodes:
                    self.set_author(i, unit)
            elif name == 'bacch:config' and unit == 'master':
                self.set_config(i, unit)

        self.info = info

    def set_config(self, node, unit):
        font = self.fetch_attr(node, 'bacch:font', '12pt')
        self.config = {
                "font": font
                }


    def fetch_attr(self, node, key, value):
        if node.hasAttribute(key):
            return node.getAttribute(key)
        else:
            return default


    def set_author(self, node, unit):
       first = other = sur = ''
       for author in node.childNodes:
            if author.nodeName == 'personname':
                for person in author.childNodes:
                    for name in person.childNodes:
                        kind = name.nodeName
                        if kind == 'firstname':
                            first = self.fetch(name)
                        elif kind == 'othername':
                            other = self.fetch(name)
                        elif kind == 'surname':
                            sur = self.fetch(name)
            fullname = first + other + sur
            author = {
                "fullname": fullname, 
                "surname": sur
                }
            self.info[unit]['authors'].append(author)

    def depart_info(self, node):
        pass

    def visit_para(self, node):
        self.body.append('\n\n')
        return True

    def depart_para(self, node):
        self.body.append('\n\n')


    #########################################
    # Process Inline
    def visit_emphasis(self, node):
        self.body.append('\\emph{')
        return True
    def depart_emphasis(self, node):
        self.body.append('}')
