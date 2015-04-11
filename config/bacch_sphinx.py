#!/usr/bin/env python3

#####################################
# Module Imports
import codecs, os.path,re, subprocess

from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.compat import Directive

from docutils import nodes, writers
from docutils.io import StringOutput


class BacchBuilder(Builder):
    
    name = "bacch"
    format = "latex"
    extension = ".tex"
    writer = None

    def init(self):
        pass

    def get_outdated_docs(self):
        return 'all documents'

    def prepare_writing(self,docnames):
        self.writer = BacchWriter(self.config)
    
    def get_relative_uri(self,from_,to,typ=None):
        return self.get_target_uri(to,typ)

    def get_target_uri(self,docname,typ):
        return '%' + docname

    def write(self, *ignored):
        docnames = self.env.all_docs

        self.info(bold("Preparing documents..."),nonl=True)
        self.prepare_writing(docnames)
        self.info("Done")

        self.info(bold("Assembling single document..."),nonl=True)
        doctree = self.assemble_doctree()
        self.info("Done")
        self.info()
        self.info(bold("Writing..."),nonl=True)
        self.write_doc(self.config.master_doc,doctree)
        self.outfile = os.path.join(
            self.outdir,os_path(
                self.config.master_doc) + self.extension)
        self.docfile = os.path.join(
            self.outdir,os_path(self.config.master_doc) + '.pdf')

        ensuredir(os.path.dirname(self.outfile))
        self.write_file(self.outfile,self.writer.output)
        self.info("Done")

    def assemble_doctree(self):
        master = self.config.master_doc
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self,set(),master,tree,darkgreen)
        tree['docname'] = master
        
        return tree

    def write_doc(self,docname,doctree):
        destination = StringOutput(encoding = 'utf-8')
        output = self.writer.write(doctree,destination)

    def write_file(self,outfile,content):
        try:
            f = codecs.open(outfile,'w','utf-8')
            try:
                f.write(content)
            finally:
                f.close()
        except (IOError,OSError) as err:
            self.warn("Error writing file %s: %s" % (outfile, err))

    def finish(self):

        # Convert LaTeX File into PDF
        command = ['pdflatex',
                   '-output-directory',
                   self.outdir,
                   self.outfile]
        subprocess.call(command)

        # Move New File from build dir 
        title = self.config.bacch_title.lower().replace(' ','') + '.pdf'
        newfile = self.srcdir + '/../' + title
        basepdf = self.outdir + '/' + self.config.master_doc + '.pdf'
    
        os.rename(basepdf, newfile)


###################################
# BacchWriter Function
class BacchWriter(writers.Writer):

    def __init__(self,config):
        writers.Writer.__init__(self)
        self.config = config

    def translate(self):
        translator = BacchTranslator(self.document,self.config)
        self.document.walkabout(translator)
        self.output = translator.astext()


#####################################
# Bacch Translator Class
class BacchTranslator(nodes.NodeVisitor):

    body = []

    def __init__(self, document, config):
        nodes.NodeVisitor.__init__(self,document)
        self.current_chapter = ''
        self.current_command = ''
        self.chapheader = {}
        self.config = config
        self.build = self.config.bacch_build_type
        self.assign_node_handlers()

    def astext(self):
        return ''.join(self.body)

    
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
            ('topic', 'skip'),
            ('transition', 'skip'),
            ('versionmodified', 'skip')
        ]
        for name in nodenames:
            if name[1] == 'skip':
                setattr(self, 'visit_' + name[0], skip_me)
            elif name[1] == 'pass':
                setattr(self, 'visit_' + name[0], pass_me)
                setattr(self,'depart_' + name[0], pass_me)
            else:
                raise ValueError("When assigning node handlers, you must set"
                                 "%s to either 'skip' or 'pass'." % name[0])


    def visit_Text(self,node):
        reserved_latex_chars = '[{}\\\^&\%\$#~_]'
        text = re.sub(reserved_latex_chars,self.escaped_chars,node.astext())
        self.body.append(text)

    def escaped_chars(self,match):
        if match.group(0) == '~':
            return '$\\sim$'
        elif match.group(0) == '\\':
            return '$\\backslash$'
        elif match.group(0) == '^':
            return '\\^{}'
        else:
            return '\\' + match.group(0)
    
    def depart_Text(self,node):
        pass


    def visit_paragraph(self,node):
        self.body.append('\n')

    def depart_paragraph(self,node):
        self.body.append('\n')


    def visit_section(self,node):

        # Establish Defaults
        parent_start = ''

        # Identify First Level Elements
        if isinstance(node.parent,nodes.document):
            
            # Discern Chapters from Index
            parent_start = str(node.parent)[0:26]
            if 'index' not in parent_start:
                self.generate_secheader(node,"chapter")

            # Identify Second Level Elements
        elif isinstance(node.parent.parent,nodes.document):
            parent_start = str(node.parent.parent)[0:26]
            if 'index' in parent_start:
                self.generate_secheader(node,"part")
            else:
                self.generate_secheader(node,"section")

        elif isinstance( node.parent.parent.parent, nodes.document):
            parent_start = str(node.parent.parent.parent)[0:26]
            if 'index' in parent_start:
                self.generate_secheader(node,"chapter")
            else:
                self.generate_secheader(node,"subsection")

    def generate_secheader(self,node,headertype):

        title = node.next_node()
        header = ""
        
        if isinstance(title,nodes.title):
            title = title.astext()

            if headertype == "part":
                header = (
                    "\\part%s{%s}\n"
                    "\n") % (
                        self.config.bacch_section_numbering,
                        title)

            elif headertype == "chapter":
                self.current_command = title.replace(" ","")
                self.current_chapter = title
                header = (
                    "\\newpage"
                    "\\chapter%s{%s}\n"
                    "\\phantomsection"
                    "\\addcontentsline{toc}{chapter}"
                    "{\\protect \\normalsize {%s}}"
                    "\n" ) % ( self.config.bacch_section_numbering,
                               title, title)
                if self.config.bacch_chaphead == "none":
                    pass
                elif self.config.bacch_chaphead == "block":
                    block = (
                        "\\singlespace\n"
                        "\\textbf{"
                        "\\scriptsize\\%s}"
                        "\\vspace{2em}\n"
                        "\n \\noindent") % (self.current_command)
                    header = header + block
                    self.chapheader[self.current_command] = [title]

                elif self.config.bacch_chaphead == "title-block":

                    heading = ("\\begin{center}\n"
                               "\\vspace{1em}"
                               "\\uppercase{"
                               "\\textls[400]{\\bfseries{%s}}}"
                               "\\vspace{2em}\n"
                               "\\end{center}"
                               "\n") % title
                    block = (
                        "\\singlespace\n"
                        "\\textbf{"
                        "\\scriptsize\\%s}"
                        "\\vspace{2em}\n"
                        "\n \\noindent") % (self.current_command)
                    header = header + heading + block
                    self.chapheader[self.current_command] = []

            elif headertype == 'section':
                header = "\\section%s{%s}" % (
                    self.config.bacch_section_numbering,
                    title)
                if self.config.bacch_chaphead == 'none':
                    pass
                elif self.config.bacch_chaphead == 'block' or self.config.bacch_chaphead == "title-block":
                    self.chapheader[self.current_command].append(title)
                    
            elif headertype == 'subsection':
                header = "\\subsection%s{%s}" % (
                    self.config.bacch_section_numbering,
                    title)
                if self.config.bacch_chaphead == 'none':
                    pass
                elif self.config.bacch_chaphead == 'block' or self.config.bacch_chaphead == "title-block":
                    self.chapheader[self.current_command].append(title)

                self.body.append(header)
        else:
            return SyntaxError(
                "This %s does not have a title." % header)

        self.body.append(header)
        
    def depart_section(self,node):
        pass

    def visit_document(self,node):
        start = []
        start.append("\\begin{document}\n")
        
        titleformat = self.config.bacch_titlepage_format

        if titleformat == 'novel-0.1':
            titlepage =("\\begin{titlepage}\n"
                        "\\begin{center}\n\n"
                        "\\showhrule\\par"
                        "\\vspace{5em}"
                        "\\bfseries \\Huge"
                        "\\textrm{"
                        "\\showuptitle}\\par"
                        "\n\n"
                        "\\vspace{8em}\\large\n"
                        "\\textrm{\\emph{\\showsubtitle}}\n\n"
                        "\\vspace{5em}\\Large\n"
                        "\\showauthor\n"
                        "\\vspace{1.5em}\n"
                        "\\showhrule\n\n"
                        "\\end{center}\n"
                        "\\end{titlepage}\n")
            start.append(titlepage)

        start.append("\n"
                     "\\setcounter{tocdepth}{5}\n")
        if self.config.bacch_show_toc:
            start.append('\\tableofcontents \n')

        for i in start:
            self.body.append(i)


    def depart_document(self,node):
        self.header = BacchHeader(self.config,self.chapheader)
        self.body.insert(0,self.header.astext())
        self.body.append('\n \\end{document}\n')

    def visit_strong(self,node):
        self.body.append('\\textbf{')

    def depart_strong(self,node):
        self.body.append('}')

    def visit_emphasis(self,node):
        self.body.append('\\emph{')

    def depart_emphasis(self,node):
        self.body.append('}')

    def visit_line_block(self,node):
        self.body.append("\n\\begin{singlespace}"
                         "\\begin{verse}")

    def depart_line_block(self,node):
        self.body.append("\n\\end{verse}"
                         "\\end{singlespace}\n")

    def visit_line(self,node):
        self.body.append('\n')

    def depart_line(self,node):
        next_line = node.next_node(condition=nodes.line,siblings=1)
        if self.line_is_blank(node) and self.line_is_blank(next_line):
            self.body.append('\\\\')

    def line_is_blank(self,node):
        if not isinstance(node,nodes.line):
            return False
        else:
            if node.astext().strip() != '':
                return True
            else:
                return False

    def visit_block_quote(self,node):
        self.body.append('\n\\begin{quotation}')

    def depart_block_quote(self,node):
        self.body.append('\n\\begin{quotation}')

    def visit_synopsis(self,node):
        self.body.append('\n\\begin{synopsis}')

    def depart_synopsis(self,node):
        self.body.append('\n\\end{synopsis}\n')


class BacchHeader(object):

    header = []

    def __init__(self,config,chapheader):
        self.config = config
        self.chapheader = chapheader

    def astext(self):
        self.set_documentclass()
        self.set_packages()
        self.set_commands()
        return '\n'.join(self.header)



    def set_documentclass(self):

        options = ['openright','pdftex']

        # Check If Nonsubmission
        if self.config.bacch_nonsubmission:
            options.append('nonsubmission')
            if self.config.bacch_notitle:
                options.append('notitle')

        # Check Quotation Type
        quote_type = self.config.bacch_quote_type
        if quote_type:
            options.append(quote_type)

        config_font = self.config.bacch_font_size
        if config_font in ['10pt', '12pt']:
            options.append(config_font)
            
        options = ','.join(options)
        
        self.header.append('\\documentclass[%s]{%s}' % (options, 'book'))


    # Configure LaTeX Packages
    def set_packages(self):

        packages = { "hyperref" : [''],
                     "titlesec" : ['explicit', 'noindentafter'],
                     "titletoc" : [''],
                     "fancyhdr" : [''],
                     "setspace" : [''] }

        # Deifine Paper Sizes
        build_type = self.config.bacch_build_type
        if build_type == 'manuscript':
            packages["geometry"] = ['letterpaper']
        elif build_type == 'book':
            packages["geometry"] = ['b5paper']

        packages["microtype"] = ["tracking"]

        for key in packages:
            if packages[key] == ['']:
                self.header.append('\\usepackage{%s}\n' % key)
            else:
                package_options = ','.join(packages[key])
                self.header.append('\\usepackage[%s]{%s}'
                                   '\n' % (package_options, key))

    # Set up LaTeX Commands
    def set_commands(self):
        commands = []

        #######################
        # Define Metadata

        commands.append(
            self.def_command(0,'showauthor',
                             self.config.bacch_author))
        commands.append(
            self.def_command(0,'showsurname',
                             self.config.bacch_surname))
        commands.append(
            self.def_command(0,'showtitle',
                             self.config.bacch_title))
        commands.append(
            self.def_command(0,'showuptitle',
                             self.config.bacch_title.upper()))
        commands.append(
            self.def_command(0,'showrunningtitle',
                             self.config.bacch_running_title))
        commands.append(
            self.def_command(0,'showscondtitle',
                             self.config.bacch_title_secondline))
        commands.append(
            self.def_command(0,'showsubtitle',
                             self.config.bacch_subtitle))

        commands.append('\\frenchspacing')


        
        # Format Section Headers
        commands.append("\\titleclass{\\part}{page}\n"
                        "\\titleformat{\\part}\n"
                        "{\\Huge}{\\thepart}{}\n"
                        "{\\centering \\uppercase{"
                        "\\textrm{\\textbf{#1}}}}\n")
        
        if len(self.chapheader) > 0:
               for key in self.chapheader:
                   call = "\\%s" % key
                   separator = self.config.bacch_chapblock_separator
                   block = separator.join(self.chapheader[key]) + "."

                   commands.append(
                       self.def_command(0, key,
                                        block))

        commands.append("\\titleclass{\\chapter}{straight}\n"
                        "\\titleformat{\\chapter}\n"
                        "{}{\\thechapter}{}{}\n"
                        "\\titlespacing{\\chapter}\n"
                        "{\\parindent}{\\baselineskip}{-2em}"
                        "\n")

        
        commands.append("\\titleclass{\\section}{straight}\n"
                    "\\titleformat{\\section}\n"
                    "{}{\\thesection}{}{\\centering \\showsecbreak} \n"
                    "\\titlespacing{\\section}\n"
                    "{\\parindent}{1em}{1em}"
                    "\n")
        commands.append("\\titleclass{\\subsection}{straight}\n"
                    "\\titleformat{\\subsection}\n"
                    "{}{\\thesubsection}{}{} \n"
                    "\\titlespacing{\\subsection}\n"
                    "{\\parindent}{\\baselineskip}{-1em}"
                    "\n")

               
        # Define Breaks
        secbreak_type = self.config.bacch_secbreak
        secbreak = ''
        if secbreak_type == 'short_line':
            secbreak = '\\rule{5em}{0.25mm}'
        commands.append(
            self.def_command(0, 'showsecbreak',
                             secbreak))

        commands.append(
            self.def_command(0, 'showhrule',
                             '\\rule{\\linewidth}{0.5mm}\n'))

                             
               

        ########################
        # Define Page Style
        commands.append("\\pagestyle{fancy}\n")

        headfoot_size = '\\%s' % self.config.bacch_headfoot_size
        headfoot_space = '\\vspace{%sem}' % self.config.bacch_headfoot_space
        headfoot_divider = self.config.bacch_headfoot_divider
        
        header_type = self.config.bacch_header_type
        if header_type == 'surname-title':
            commands.append("\\fancyhead[LE]{"
                            "%s \\showsurname %s"
                            "}" % (headfoot_size,headfoot_space))
            commands.append("\\fancyhead[RO]{"
                            "%s \\showrunningtitle %s"
                            "}" % (headfoot_size, headfoot_space))

        elif header_type == 'title-surname':
            commands.append("\\fancyhead[RO]{"
                            "%s \\showsurname %s"
                            "}" % (headfoot_size,headfoot_space))
            commands.append("\\fancyhead[LE]{"
                            "%s \\showrunningtitle %s"
                            "}" % (headfoot_size, headfoot_space))

        elif header_type == 'title-and-surname':
            commands.append("\\fancyhead[RO]{"
                            "%s \\showrunning_title %s \\showsurname %s"
                            "}" % (headfoot_size, headfoot_divider,
                                   headfoot_space))
            commands.append("\\fancyhead[LE]{"
                            "%s \\showsurname %s \\showrunning_title %s"
                            "}" % (headfoot_size, headfoot_divider,
                                   headfoot_space))

        elif header_type == 'surname-and-title':
            commands.append("\\fancyhead[LE]{"
                            "%s \\showrunning_title %s \\showsurname %s"
                            "}" % (headfoot_size, header_divider, headfoot_space))
            commands.append("\\fancyhead[RO]{"
                            "%s \\showsurname %s \\showrunning_title %s"
                            "}" % (headfoot_size, headfoot_divider,
                                   headfoot_space))
        else:
            commands.append("\\fancyhead[RO,LE]{"
                            "%s" % (headfoot_space))
        # Define Footer
        footer_type = self.config.bacch_header_type
        if footer_type == 'pagenumber':
            commands.append('\\fancyfoot[RO,LE]{'
                            '%s \\thepage %s' % (headfoot_size, headfoot_space))
        

        for command in commands:
            self.header.append(command)
        
            
    # Define Command
    def def_command(self, typ, variable, values):

        # Define New Commands
        if typ == 0:
            return "\\newcommand{\\%s}{%s}\n" % (variable, values)
        # Define Renew Commands
        elif typ == 1:
            return "\\renewcommand{\\%s}{%s}\n" % (variable,value)


            

        

    

    

##################################
# Register Docutiles Node Classes
def add_nodes(app):

    app.add_node(suppress_numbering,
                 html=(skip_me, None), latex=(skip_me,None),
                 text=(skip_me, None), man=(skip_me,None))
    app.add_directive('suppress_numbering',SuppressNumberingDirective)

    app.add_node(synopsis,
                 html=(pass_me,pass_me),
                 latex = (pass_me,pass_me),
                 text = (pass_me, pass_me),
                 man = (pass_me,pass_me))
    app.add_directive('suppress_synopsis', SynopsisDirective)

def skip_me(node):
    raise nodes.SkipNode

def pass_me(node):
    pass

class suppress_numbering(nodes.General, nodes.Element):
    pass

class synopsis(nodes.Structural, nodes.Element):
    pass

class SuppressNumberingDirective(Directive):
    def run(self):
        return [ suppress_numbering('') ]

class SynopsisDirective(Directive):
    
    node_class = synopsis
    has_content = True

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        synopsis_node = self.node_class(rawsource = text)
        self.state.nested_parse(self.content,
                                self.content_offset,
                                synopsis_node)
        return [ synopsis_node ]



################################
# Setup Module
def setup(app):
    print("Initializing bacch-Sphinx Builder extension.")
    app.add_builder(BacchBuilder)

    # Custom nodes, roles and directives.
    add_nodes(app)

    # Define Project Variables
    app.add_config_value('bacch_build_type',None,'')

    # Define Typesetting Variables
    app.add_config_value('bacch_section_numbering','*','')
    app.add_config_value('bacch_chaphead', 'title-block', '')
    app.add_config_value('bacch_titlepage_format','novel-0.1','')
    app.add_config_value('bacch_show_toc', True,'')

    app.add_config_value('bacch_nonsubmission', None,'')
    app.add_config_value('bacch_quote_type','smart','')
    app.add_config_value('bacch_notitle',False,'')
    app.add_config_value('bacch_secbreak','short_line','')

    app.add_config_value('bacch_headfoot_size','tiny','')
    app.add_config_value('bacch_headfoot_space','2','')
    app.add_config_value('bacch_headfoot_divider','|','')
    app.add_config_value('bacch_header_type','surname-title','')
    app.add_config_value('bacch_footer_type','pagenumber','')
    app.add_config_value('bacch_chapblock_separator',' -- ','')
    app.add_config_value('bacch_frenchspacing',True,'')
    app.add_config_value('bacch_font_size','10pt','')
    
    # Define Metadata Variables
    app.add_config_value('bacch_author',None,'')
    app.add_config_value('bacch_surname',None,'')
    app.add_config_value('bacch_title',None,'')
    app.add_config_value('bacch_running_title',None,'')
    app.add_config_value('bacch_subtitle',None,'')
    app.add_config_value('bacch_title_secondline',None,'')
                         



