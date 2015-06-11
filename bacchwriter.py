#! /usr/bin/env python3

import codecs, os.path, re, subprocess

from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.compat import Directive

from docutils import nodes, writers
from docutils.io import StringOutput



class BacchWriter(writers.Writer):

    def __init__(self, config, outclass):
        writers.Writer.__init__(self)
        self.config = config
        self.outclass = outclass

    def translate(self):
        translator = BacchTranslator(self.document, self.config, self.outclass)
        self.document.walkabout(translator)
        self.output = translator.astext()


class BacchTranslator(nodes.NodeVisitor):

    body = []
    def __init__(self, document, config, outclass):
        nodes.NodeVisitor.__init__(self, document)
        self.config = config
        self.outclass = outclass

        self.chapheader = {}
        self.current_chapter = ''
        self.section_level = 0
        self.header = []
        self.open = False
        
        # Build Calls
        self.assign_node_handlers()

    # Astext Return Value
    def astext(self):
        return ''.join(self.body)

    # Handler Assignment
    def assign_node_handlers(self):

        nodenames = [
            ('abbreviation', 'skip'),
            ('acks', 'skip'),
            ('admonition', 'skip'),
            ('attribution', 'skip'),
            ('bullet_list', 'skip'),
            ('caption', 'skip'),
            ('centered', 'skip'),
            ('citation', 'skip'),
            ('citation_reference', 'skip'),
            ('classifier', 'skip'),
            ('collected_footnote', 'skip'),
            ('colspec', 'skip'),
            ('comment', 'skip'),
            ('compact_paragraph', 'skip'),
            ('compound', 'pass'),
            ('container', 'skip'),
            ('decoration', 'skip'),
            ('definition', 'skip'),
            ('definition_list', 'skip'),
            ('definition_list_item', 'skip'),
            ('desc', 'skip'),
            ('desc_addname', 'skip'),
            ('desc_annotation', 'skip'),
            ('desc_content', 'skip'),
            ('desc_name', 'skip'),
            ('desc_optional', 'skip'),
            ('desc_parameter', 'skip'),
            ('desc_parameterlist', 'skip'),
            ('desc_returns', 'skip'),
            ('desc_signature', 'skip'),
            ('desc_type', 'skip'),
            ('description', 'skip'),
            ('docinfo', 'skip'),
            ('download_reference', 'skip'),
            ('entry', 'skip'),
            ('enumerated_list', 'skip'),
            ('field', 'skip'),
            ('field_list', 'skip'),
            ('figure', 'skip'),
            ('footer', 'skip'),
            ('footnote', 'skip'),
            ('footnote_reference', 'skip'),
            ('generated', 'skip'),
            ('glossary', 'skip'),
            ('header', 'skip'),
            ('highlightlang', 'skip'),
            ('hlist', 'skip'),
            ('hlistcol', 'skip'),
            ('image', 'skip'),
            ('index', 'skip'),
            ('inline', 'skip'),
            ('label', 'skip'),
            ('legend', 'skip'),
            ('list_item', 'skip'),
            ('literal', 'skip'),
            ('literal_block', 'skip'),
            ('literal_emphasis', 'skip'),
            ('meta', 'skip'),
            ('option', 'skip'),
            ('option_argument', 'skip'),
            ('option_group', 'skip'),
            ('option_list', 'skip'),
            ('option_list_item', 'skip'),
            ('option_string', 'skip'),
            ('pending_xref', 'skip'),
            ('problematic', 'skip'),
            ('production', 'skip'),
            ('productionlist', 'skip'),
            ('raw', 'skip'),
            ('refcount', 'skip'),
            ('reference', 'skip'),
            ('row', 'skip'),
            ('rubric', 'skip'),
            ('seealso', 'skip'),
            ('start_of_file', 'pass'),
            ('subscript', 'skip'),
            ('substitution_definition', 'skip'),
            ('substitution_reference', 'skip'),
            ('subtitle', 'skip'),
            ('superscript', 'skip'),
            ('suppress_numbering', 'pass'),
            ('system_message', 'skip'),
            ('table', 'skip'),
            ('tabular_col_spec', 'skip'),
            ('target', 'skip'),
            ('tbody', 'skip'),
            ('term', 'skip'),
            ('tgroup', 'skip'),
            ('thead', 'skip'),
            ('title', 'skip'),
            ('title_reference', 'skip'),
            ('todo','pass'),
            ('topic', 'skip'),
            ('transition', 'skip'),
            ('versionmodified', 'skip'),
        ]

        for name in nodenames:
            if name[1] == 'skip':
                setattr(self, 'visit_' + name[0], skip_me)
            elif name[1] == 'pass':
                setattr(self, 'visit_' + name[0], pass_me)
                setattr(self, 'depart_' + name[0], pass_me)
            else:
                raise ValueError("When assigning node handlers, you must set"
                                 "%s to either 'skip' or 'pass'." % name[0])

    ########################################
    # Parse Text
    def visit_Text(self, node):
        reserved_latex_chars = '["{}\\\^&\%\$#~_]'
        text = re.sub(reserved_latex_chars, self.escaped_chars, node.astext())
        self.body.append(text)

    def escaped_chars(self, match):
        if match.group(0) == '~':
            return '$\\sim$'
        elif match.group(0) == '\\':
            return '$\\backslash$'
        elif match.group(0) == '^':
            return '\\^{}'
        elif match.group(0) == '"':
            if self.open == True:
                self.open = False
                return "''"
            else:
                self.open = True
                return "``"
        else:
            return '\\' + match.group(0)

    def depart_Text(self, node):
        pass

    ########################################
    # Parse Paragraph
    def visit_paragraph(self, node):
        self.body.append('\n')

    def depart_paragraph(self, node):
        self.body.append('\n')

    ########################################
    # Parse Section
    def visit_section(self, node):
        self.manage_section(node, True)

    def depart_section(self, node):
        self.manage_section(node, False)

    def manage_section(self, node, arrive):
        out = self.outclass
        if out == "fullbacch":
            if arrive:
                self.full_section_opener(node)
            else:
                self.full_section_closer(node)

                

    def full_section_opener(self, node):
        # Initialize Checks
        docname = node.get('docname')
        if docname == None:
            docname = 'index'

        parent_start = ''

        if 'part' in docname:
            self.section_level = 1
            self.generate_secheader(node, "part")
                
        elif isinstance(node.parent, nodes.document):
            # Discern Chapters and Parts from Index
            parent_start = str(node.parent)[0:30]

            if 'index' not in parent_start:
                self.section_level = 2
                self.generate_secheader(node, "chapter")

        elif isinstance(node.parent.parent, nodes.document):
            parent_start = str(node.parent.parent)[0:26]
            if 'index' in parent_start:

                #######################################
                # Note: Write a nested conditional
                #  check here to indicate whether
                #  to generate a Part Header or a
                #  Prologue. May need additional checks
                #  to handle subsections in prologue.
                ########################################

                #self.section_level = 1
                
                self.generate_secheader(node, "part")
            else:
                self.generate_secheader(node, "section")

        elif isinstance(node.parent.parent.parent, nodes.document):
            parent_start = str(node.parent.parent.parent)[0:26]
            if 'index' in parent_start:
                self.generate_secheader(node, "chapter")
            else:
                self.generate_secheader(node, "subsection")


                
    def full_section_closer(self, node):
        pass


    def generate_secheader(self, node, headertype):
        title = node.next_node()

        if isinstance(title, nodes.title):
            title = title.astext()
            if headertype == "part":
                self.generate_parthead(title)

            elif headertype == "chapter":
                self.generate_chaphead(title)

            elif headertype == "section":
                self.generate_secthead(title)
            elif headertype == "subsection":
                self.generate_subsecthead(title)


    def generate_parthead(self, title):
        header = ''
        header = "\\part*{%s}\n" % title
        content = ('\\phantomsection\n'
                   '\\addcontentsline{toc}{chapter}'
                   '{\\protect \\small %s }\n') % title
        header = header #+ content
        self.body.append(header)

    def generate_chaphead(self, title):
        header = block = topblock = ''
        blocktype = self.config.bacch_chapter_block
        command = title.replace(' ','')
        self.current_chapter = title
        header = '\\chapter*{%s}\n' % title

        end =('\\phantomsection\n'
              '\\addcontentsline{toc}{chapter}'
              '{\\protect \\small -- %s}\n'
              '\n') % (title)
        header = '\\newpage\n' + header + end

        blocktop = ('\\begin{center}\n'
                    '\\vspace{1em}'
                    '\\uppercase{'
                    '\\textls[400]{\\bfseries{%s}}}'
                    '\\vspace{2em}\n'
                    '\\end{center}'
                    '\n') % title

        block = ('\\singlespace\n'
                 '\\textbf{'
                 '\\scriptsize\\%s}'
                 '\\vspace{2em}\n'
                 '\n \\noindent') % command

        if blocktype == 'block':
            header = header + block
            self.chapheader[title] = [title]
        elif blocktype == 'title-block':
            header = header + blocktop + block
            self.chapheader[title] = []
        elif blocktype == 'titleonly':
            header = header + blocktop
        self.body.append(header)


    def generate_secthead(self, title):
        header = ''
        blocktype = self.config.bacch_chapter_block

        header = '\\section*{%s}\n' % title
        
        if blocktype == 'title-block' or blocktype == 'block':
            self.chapheader[self.current_chapter].append(title)
        self.body.append(header)

    def generate_subsecthead(self, title):
        header = ''
        blocktype = self.config.bacch_chapter_block
        header = '\\subsection*{%s}\n' % title
        if blocktype == 'title-block' or blocktype == 'block':
            self.chapheader[self.current_chapter].append(title)
        self.body.append(header)



    ##############################################
    # Parse Document
    def visit_document(self, node):
        start = [ "\\begin{document}\n" ]
        out = self.outclass
        if out == "fullbacch":
            start.append(self.generate_titlepage_full())
        #start.append("\n\\setcounter{tocdepth}{-1}\n")

        if self.config.bacch_show_toc:
            start.append(#'\\usecontents{index}{toc}\n'
                '\\tableofcontents\n\n'
            )

        self.body.append('\n'.join(start))

    def depart_document(self, node):
        self.header = BacchHeader(self.config, self.chapheader, self.outclass)
        self.body.insert(0, self.header.astext())
        self.body.append('\n \\end{document}\n')


    def generate_titlepage_full(self):

        titlepage = ('\\begin{titlepage}\n'
                     '\\begin{center}\n \\showhrule\\par \\vspace{5em}'
                     '\\bfseries \\Huge \\textrm{ \\showuptitle} \\par \n\n'
                     '\\vspace{8em} \\large \\textrm{\\emph{\\showsubtitle}}\n\n'
                     '\\vspace{5em} \\Large \\showauthor \n'
                     '\\vspace{1.5em} \\showhrule \n\n'
                     '\\end{center}\n \\end{titlepage}\n')

        return titlepage


    # Parse Inline Formatting
    def visit_strong(self, node):
        self.body.append('\\textbf{')

    def depart_strong(self, node):
        self.body.append('}')

    def visit_emphasis(self, node):
        self.body.append('\\emph{')

    def depart_emphasis(self, node):
        self.body.append('}')


    # Parse Verse
    def visit_line_block(self, node):
        self.body.append('\n\\begin{singlespace} \\begin{verse}\n')

    def depart_line_block(self, node):
        self.body.append('\n\\end{verse}\\end{singlespace}\n')

    def visit_line(self, node):
        self.body.append('\n')

    def depart_line(self, node):
        next_line = node.next_node(condition=nodes.line, siblings=1)
        if self.line_is_blank(node) and self.line_is_blank(next_line):
            self.body.append('\\\\')

    def line_is_blank(self, node):
        if not isinstance(node, nodes.line):
            return False
        else:
            if node.astext().strip() != '':
                return True
            else:
                return False

    # Parse Block Quote
    def visit_block_quote(self, node):
        self.body.append('\n\\begin{quotation}\n')

    def depart_block_quote(self, node):
        self.body.append('\n\\end{quotation}\n')

    # Parse Todos
    def visit_note(self, node):
        header = ('\\begin{framed}'
                  '\\small\n \\noindent'
                  '\\textbf{Note: }')

        note = header
        self.body.append(note)
    def depart_note(self, node):
        note = ('\\end{framed}\n')
        self.body.append(note)

###################################################
# Generate LaTeX Header Information
class BacchHeader(object):
    header = []

    def __init__(self, config, chapheader, outclass):
        self.config = config
        self.chapheader = chapheader
        self.outclass = outclass

        self.set_documentclass()
        self.set_packages()
        self.set_commands()


    def astext(self):
        return '\n'.join(self.header)


    # Generate DocumentClass Variables
    def set_documentclass(self):

        # Initialize Options with Defaults
        options = ['openright', 'pdflatex', 'notitlepage','twoside']

        config_font = self.config.bacch_font_size
        if config_font in ['10pt', '12pt']:
            options.append(config_font)

        options = ','.join(options)
        self.header.append('\\documentclass[%s]{%s}\n'
                           % (options, 'book'))


    # Generate Package Variables
    def set_packages(self):
        out = self.outclass
        # Initialize Default Packages
        packages = {#'hyperref' : ['implicit=true'],
                    'titlesec': ['explicit', 'noindentafter'],
                    'fancyhdr': [''],
                    'setspace': [''],
                    'framed': [''],
                    'microtype': ['tracking'],
                    #'inputenc':['utf8'],
                    #'cmap':[''],
                    #'times':[''],
                    #'longtable':[''],
                    #'multirow':[''],
                    'bookmark':['']
        }

        buildtype = self.config.bacch_buildtype
        if out == "fullbacch" and buildtype == 'TPB':
            packages["geometry"] = ['b5paper']
        elif out == "fullbacch" and buildtype == 'SMF':
            packages["geometry"] = ["letterpaper"]
        else:
            packages["geometry"] = ["letterpaper"]

        for key in packages:
            if packages[key] == ['']:
                self.header.append('\\usepackage{%s}\n' % key)
            else:
                self.header.append('\\usepackage[%s]{%s}\n'
                                   % (','.join(packages[key]), key))



    # Generate Command Variables
    def set_commands(self):
        out = self.outclass
        newcommands = {
            'showauthor': self.config.bacch_author,
            'showsurname': self.config.bacch_surname,
            'showtitle': self.config.bacch_title,
            'showuptitle': self.config.bacch_title.upper(),
            'showruntitle': self.config.bacch_title_runner,
            'showsecondtitle': self.config.bacch_title_second,
            'showsubtitle':self.config.bacch_title_subtitle,
        }

        renewcommands = {}

        # Write Commands to Header
        commands = {'new': newcommands,
                    'renew': renewcommands}

        for i in commands:
            for key in commands[i]:
                self.def_command(i, key, commands[i][key])


        # Add Nonvariable Commands
        self.header.append('\\frenchspacing')

        # Format Section Headers
        if out == "fullbacch":
            self.full_secheaders()


        # Format Section Breaks
        secbreak_type = self.config.bacch_secbreak
        if secbreak_type == 'short_line':
            secbreak = ('\\vspace{1em}'
                        '\\rule{5em}{0.25mm}'
                        '\\vspace{1em}'
            )
        else:
            secbreak = ''
        self.def_command('new', 'showsecbreak', secbreak)

        showhrule = '\\rule{\\linewidth}{0.5mm}\n'
        self.def_command('new', 'showhrule', showhrule)

        # Configue Page Style
        if out == "fullbacch":
            self.full_page_styler()


    def def_command(self, command_type, variable, value):
        if command_type == 'new':
            self.header.append('\\newcommand{\\%s}{%s}'
                               '\n' % (variable, value))
        elif command_type == 'renew':
            self.header.append('\\renewcommand{\\%s}{%s}'
                               '\n' % (variable, value))


    def full_secheaders(self):
        # Format Part Header
        self.header.append('\\titleclass{\\part}{page}\n'
                           '\\titleformat{\\part}'
                           '{\\Huge}{\\thepart}{}'
                           '{\\centering \\uppercase{'
                           '\\textrm{\\textbf{#1}}}}\n'
        )

        # Format Chapter Header Blocks

        if len(self.chapheader) > 0:
            for key in self.chapheader:
                separator = self.config.bacch_chapblock_separator
                block = separator.join(self.chapheader[key]) + '.'
                self.def_command('new', key.replace(' ',''), block)

        # Format Chapter Header
        self.header.append('\\titleclass{\\chapter}{straight}\n'
                           '\\titleformat{\\chapter}'
                           '{}{\\thechapter}{}{}\n'
                           '\\titlespacing{\\chapter}'
                           '{\\parindent}{\\baselineskip}{0em}\n'
        )

        # Format Section Header
        self.header.append('\\titleclass{\\section}{straight}\n'
                           '\\titleformat{\\section}'
                           '{}{\\thesection}{}'
                           '{\\centering \\showsecbreak}\n'
                           '\\titlespacing{\\section}'
                           '{\\parindent}{1em}{1em}\n')

        # Format Subsection Header
        self.header.append('\\titleclass{\\subsection}{straight}\n'
                           '\\titleformat{\\subsection}\n'
                           '{}{\\thesubsection}{}{}\n'
                           '\\titlespacing{\\subsection}\n'
                           '{\\parindent}{\\baselineskip}{-1em}\n')


    def full_page_styler(self):
        self.header.append('\\pagestyle{fancy}\n')

        headfoot_size = '\\' + self.config.bacch_headfoot_size
        headfoot_space = '\\vspace{%s}' % self.config.bacch_headfoot_space
        headfoot_divider = self.config.bacch_headfoot_divider

        header_type = self.config.bacch_header_type

        clear = "\\fancyhead{} \\fancyfoot{}"
        command = ''
        if header_type == 'surname-title':
            command1 = ('\\fancyhead[LE]{'
                       '%s \\showsurname %s}'
                       '\n' % (headfoot_size, headfoot_space))
            command2 = ('\\fancyhead[RO]{'
                        '%s \\showruntitle %s}'
                        '\n' % (headfoot_size, headfoot_space))
            command = command1 + command2

        elif header_type == 'title-surname':
            command1 = ('\\fancyhead[LE]{'
                        '%s \\showruntitle %s}'
                        '\n' % (headfoot_size, headfoot_space))
            command2 = ('\\fancyhead[RO]{'
                        '%s \\showsurname %s}'
                        '\n' % (headfoot_size, headfoot_space))
            command = command1 + command2

        elif header_type == 'title-and-surname':
            command1 = ('\\fancyhead[RO]{'
                        '%s \\showruntitle %s \\showsurname %s}'
                        '\n' % (headfoot_size, headfoot_divider, headfoot_space))
            command2 = ('\\fancyhead[LE]{'
                        '%s \\showsurname %s \\showruntitle %s}'
                        '\n' % (headfoot_size, headfoot_divider, headfoot_space))
            command = command1 + command2

        elif header_type == 'surname-and-title':
            command1 = ('\\fancyhead[LE]{'
                        '%s \\showruntitle %s \\showsurname %s}'
                        '\n' % (headfoot_size, headfoot_divider, headfoot_space))
            command2 = ('\\fancyhead[RO]{'
                        '%s \\showsurname %s \\showruntitle %s}'
                        '\n' % (headfoot_size, headfoot_divider, headfoot_space))
            command = command1 + command2
        else:
            command = '\\fancyhead[RO,LE]{%s}' % headfoot_space

        self.header.append(clear + command)

        # Format Footer
        command = ''
        footer_type = self.config.bacch_footer_type
        if footer_type == 'pagenumout':
            command =  ('\\fancyfoot[RO,LE]{'
                        '%s \\thepage %s'
                        '}' % (headfoot_size, headfoot_space))

        self.header.append(command)




############################
# General Functions

def skip_me(node):
    raise nodes.SkipNode

def pass_me(node):
    pass
