import re


#################################
# PDF Translator
class PDFTranslator():

    def __init__(self, config):
        self.config = config
        self.document = []
        self.level = -1
        self.open_quotes = False

        


    def visit_Text(self, node):
        reserved_latex_chars = '["{}\\\^&\%\$#~_]'
        text = re.sub(reserved_latex_chars,
                    self.escaped_chars,
                    node.astext())
        self.document.append(text)

    def depart_Text(self, node):
        pass


    def escaped_chars(self, match):
        if match.group(0) == '~':
            return '$\\sim$'
        elif match.group(0) == '\\':
            return '$\\backslash$'
        elif match.group(0) == '^':
            return '\\^{}'
        elif match.group(0) == '"':
            if self.open_quotes == True:
                self.open_quotes = False
                return "''"
            else:
                self.open_quotes = True
                return "``"
        else:
            return '\\' + match.group(0)

    
    def visit_paragraph(self, node):
        self.document.append('\n')
    
    def depart_paragraph(self, node):
        self.open_quotes = False
        self.document.append('\n')

    def visit_section(self, node):        
        self.level += 1
        title = node.next_node().astext()
        sections = ['chapter', 'section', 'subsection',
                    'subsubsection', 'paragraph', 'subparagraph']
        section = sections[self.level]
        base = '\\%s*{%s}\n\n' % (section, title)
        
        build_type = self.config.bacch_build_type
        config = getattr(self.config, '%s_%s_format' % (build_type, section))

        if config['contents_use']:
            base += '\\phantomsection \n\\addcontentsline{toc}{%s}{%s %s}\n' % (
                section, config['contents_above'], title)

        head = ''
        if config['title_use']:
            head = '\n'.join([
                config['title_prefix'],
                title, config['title_suffix']])

        if config['par_noindent']:
            head += '\n\n\\noindent'

        if build_type == 'gnomon' and section == 'section':
            self.config.section_title = title
            
        self.document.append(base + head)

    def depart_section(self, node):
        self.level += -1
        
    def visit_document(self, node):
        base = ['\\begin{document}\n']

        
        # Manage Title Page
        titlepage = ('\\begin{titlepage}\n'
                     '\\begin{center}\n\\showhrule\\par\\vspace{5em}'
                     '\\bfseries\\Huge\\textrm{\\showuptitle}\\par\n\n'
                     '\\vspace{7.25em}\\large'
                     '\\textrm{\\emph{\\showsubtitle}}\n\n'
                     '\\vspace{4.75em}\\Large\\showauthor\n\n'
                     '\\vspace{1em}\\showhrule\n\n'
                     '\\end{center}\n\n')

        build_type = self.config.bacch_build_type
        if build_type == "gnomon":
            titlepage = ('\\begin{titlepage}\n'
                         '\\showhrule\n\n'
                         '\\Large\\showsectitle\n\n'
                         '\\vspace{0.5in}\\hspace{0.5in}'
                         '\\normalsize\\showauthor\n\n'
                         '\\vspace{0.5in}\\hspace{0.5in}\\emph{From} \\showtitle')

            if self.config.bacch_subtitle != '':
                titlepage += (': \\showsubtitle\n\n')

            titlepage += (
                '\\small\\vspace{0.1in}\\hspace{1in}\\emph{Begun} '
                '\\showcreatedate\n\n'
                '\\small\\vspace{0.05in}\\hspace{1in}\\emph{Compiled} ' 
                '\\showcompiledate\n\n')
                        

        base.append(titlepage)
        # Manage Publication Line
        publisher = self.config.bacch_publisher
        cities = self.config.bacch_pubcities
        publine = ''
        if len(cities) > 0:
            cities = ' + '.join(cities)

        bottomline = ('\\end{titlepage}\n\n')
        if publisher != '' and build_type != "gnomon":
            bottomline = ('\\begin{center}'
                       '\\small \\textbf{\\emph{%s}} \n\n'
                       '\\footnotesize \\textbf{%s} \n'
                       '\\end{center} \\end{titlepage}' % (publisher, cities))
        
        base.append(bottomline)


        if self.config.bacch_show_toc == True and build_type != "gnomon":
            base.append("\\cleardoublepage\n"
                        "\\setcounter{tocdepth}{1}\n"
                        "\\tableofcontents\n\n")


        docstart = '\n'.join(base)
        self.document.append(docstart)


    def depart_document(self, node):

        # Build Headers
        header = self.set_header()
        self.document.insert(0, header)
        self.document.append('\n\n\\end{document}')

    def visit_strong(self, node):
        self.document.append('\\textbf{')

    def depart_strong(self, node):
        self.document.append('}')
    
    def visit_emphasis(self, node):
        self.document.append('\\emph{')

    def depart_emphasis(self, node):
        self.document.append('}')

    def visit_literal(self, node):
        self.document.append('\\textbf{')

    def depart_literal(self, node):
        self.document.append('}')

    def visit_literal_emphasis(self, node):
        self.document.append('\\emph{')

    def depart_literal_emphasis(self, node):
        self.document.append('}')

    # Parse Notes
    def visit_note(self, node):
        self.document.append('\\begin{framed}'
                        '\\small \\noindent')

    def depart_note(self, node):
        self.document.append('\\end{framed}\n')


    def set_header(self):

        documentclass = self.set_documentclass()
        packages = self.set_packages()
        commands = self.set_commands()
        titles = self.set_titles()
        headings = self.set_headings()

        return documentclass + packages + commands + titles + headings

    def set_documentclass(self):
        options = ['openright', 'pdflatex']
        build_type = self.config.bacch_build_type

        font_size = getattr(self.config, '%s_font_size' % build_type)
        if font_size in ['10pt', '12pt']:
            options.append(font_size)
        else:
            options.append('12pt')

        options = ','.join(options)
        return '\\documentclass[%s]{book}\n' % options

    def set_packages(self):
        packages = {
            'titlesec':     ['explicit', 'noindentafter'],
            'fancyhdr':     [''],
            'setspace':     [''],
            'titletoc':     [''],
            'framed':       [''],
            'microtype':    ['tracking'],
            'inputenc':     ['utf8'],
            'bookmark':     [''],
            'lettrine':     [''],
            'geometry':     [''],
            'textcase':     [''],
            'babel':    ['english']
        }
        build_type = self.config.bacch_build_type
        if build_type == 'bacch':
            packages['geometry'] = ['b5paper']
        elif build_type == 'gnomon':
            packages['geometry'] = ['letterpaper']

        package_list = []
        for key in packages:
            if packages[key] == ['']:
                package_list.append('\\usepackage{%s}\n' % key)
            else:
                options = ','.join(packages[key])
                package_list.append('\\usepackage[%s]{%s}\n' % (options, key))
        return '\n'.join(package_list)
                

    def set_commands(self):
        
        showhrule = '\\rule{\\linewidth}{0.5mm}\n'

        newcommands = {
            'showauthor': self.config.bacch_author,
            'showsurname': self.config.bacch_surname,
            'showtitle': self.config.bacch_title,
            'showuptitle': self.config.bacch_title.upper(),
            'showruntitle': self.config.bacch_title_runner,
            'showsecondtitle': self.config.bacch_title_second,
            'showsubtitle': self.config.bacch_subtitle,
            'showhrule': showhrule,
            'showsecbreak': '---------',
            'showcreatedate': self.config.bacch_createdate,
            "showcompiledate": self.config.bacch_compiledate
        }

        if self.config.bacch_build_type == "gnomon":
            newcommands["showsectitle"] = self.config.section_title

        command_list = ['\\frenchspacing\n']
            
        renewcommands = {}
        commands = {
            'new': newcommands,
            'renew': renewcommands }
        for i in commands:
            for key in commands[i]:
                if commands[i][key] != '':
                    command = '\\%scommand{\\%s}{%s}\n' % (
                        i, key, commands[i][key])
                    command_list.append(command)
        return '\n'.join(command_list)

    def set_titles(self):

        titles_config = []
        build_type = self.config.bacch_build_type
        if build_type == "bacch":
            titles_config = [self.config.bacch_chapter_format,
                             self.config.bacch_section_format,
                             self.config.bacch_subsection_format,
                             self.config.bacch_subsubsection_format,
                             self.config.bacch_paragraph_format,
                             self.config.bacch_subparagraph_format
            ]

        elif build_type == "gnomon":
            titles_config =[self.config.gnomon_chapter_format,
                            self.config.gnomon_section_format,
                            self.config.gnomon_subsection_format,
                            self.config.gnomon_subsubsection_format,
                            self.config.gnomon_paragraph_format,
                            self.config.gnomon_subparagraph_format
            ]

        base = []

        for var in titles_config:
            base.append('\\titleclass{\\%s}{%s}'
                        '\n' % (var["name"],
                                var["class"]))
            
            titleformat = '\\titleformat{\\%s}' % var["name"]
            shape = var["format_shape"]
            if shape != '':
                titleformat += '[%s]' % shape
            titleformat += ('{%s}{%s}{%s}{%s}'
                            '\n')  % (var["format_format"],
                                      var["format_label"],
                                      var["format_sep"],
                                      var["format_before"])
            after = var["format_after"]
            if after != '':
                titleformat += '[%s]' % after
            base.append(titleformat)
                
            base.append('\\titlespacing{\\%s}'
                        '{%s}{%s}{%s}'
                        '\n' % (var["name"],
                                var["spacing_left"],
                                var["spacing_before_sep"],
                                var["spacing_after_sep"]))


            contents_use = var["contents_use"]
            contents_left = var["contents_left"]
            if contents_use:
                contents = '\\dottedcontents{%s}' % var["name"]
                if contents_left != '':
                    contents += '[%s]' % contents_left
                contents += '{%s}{%s}{%s}' % (var["contents_above"],
                                              var["contents_label_width"],
                                              var["contents_leader_width"])
                
                base.append(contents)
            base.append('\n')

        return '\n'.join(base)

        

    def set_headings(self):
        header_format = {}
        build_type = self.config.bacch_build_type
        if build_type == "bacch":
            header_format = self.config.bacch_header_format
        elif build_type == "gnomon":
            header_format = self.config.gnomon_header_format

        heading = []

        heading.append('\\pagestyle{fancy}\n')
        heading.append('\\fancyhead{}\n\\fancyfoot{}')
        heading.append('\\renewcommand{\\headrulewidth}{%s}\n'
                           '\\renewcommand{\\footrulewidth}{%s}\n'
                           % (header_format["headrulewidth"],
                              header_format["footrulewidth"]))
        for key in header_format:
            if 'format' in key:
                kind = key.split('_')
                heading.append('\\fancy%s[%s]{%s}\n'
                                   % (kind[1], kind[2],
                                      header_format[key]))
        return '\n'.join(heading)
    
        
    def return_text(self):
        return ''.join(self.document)
        

    
