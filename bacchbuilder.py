#! /usr/bin/env python3

######################################
# Module Imports
import codecs, os.path,re, subprocess

from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.compat import Directive

from docutils import nodes, writers
from docutils.io import StringOutput




##################################
# bacch Special Builder Class 
class BacchBuilder(Builder):
    """
    Builder class for special PDF and Office Open Format
    builds in bacch.
    """

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

    # Override default write() to assemble inline doctree before
    # calling write_doc().

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
        outfile = os.path.join(self.outdir,os_path(self.config.master_doc) + self.extension)
        ensuredir(os.path.dirname(outfile))
        self.write_file(outfile,self.writer.output)
        self.generate_pdf(outfile)
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

    def finish(self):
        pass
        #self.info(bold("Copying Makefile..."), nonl=True)
        #outfile = os.path.join(self.outdir, "Makefile")
        #self.write_file(outfile,makefile_bacch)
        #self.info("Done")

    def write_file(self,outfile,content):
        try:
            f = codecs.open(outfile,'w','utf-8')
            try:
                f.write(content)
            finally:
                f.close()
        except (IOError,OSError) as err:
            self.warn("Error writing file %s: %s" % (outfile, err))

    def generate_pdf(self,outfile):
        subprocess.call(['pdflatex','build/index.tex'])



class BacchWriter(writers.Writer):
    """
    Writer class for special PDF and Office Open Format
    builds in bacch
    """
    
    def __init__(self, config):
        writers.Writer.__init__(self)
        self.config = config

    def translate(self):
        translator = BacchTranslator(self.document, self.config)
        self.document.walkabout(translator)
        self.output = translator.astext()

class BacchTranslator(nodes.NodeVisitor):
    """
    Translator class for special PDF and Office Open Format
    builds in bacch
    """
    body = []

    def __init__(self,document,config):
        nodes.NodeVisitor.__init__(self,document)
        self.current_chapter = ''
        self.chapheader = {}
        self.config = config
        self.assign_node_handlers()

    def astext(self):
        return ''.join(self.body)

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
        # Establish Default Subsection
        element = 'subsection'
        parent_start = ''

        # Identify First Level Elements
        if isinstance(node.parent,nodes.document):
            # Discern Chapters from Index
            parent_start = str(node.parent)[0:26]
            if 'index' not in parent_start:
                self.generate_header(node,"chapter")
        
        # Identify Second Level Elements
        elif isinstance(node.parent.parent,nodes.document):
            parent_start = str(node.parent.parent)[0:26]
            if 'index' in parent_start:
                self.generate_header(node, "part")
            else:
                self.generate_header(node, "section")

        elif isinstance(node.parent.parent.parent,nodes.document):
            parent_start = str(node.parent.parent.parent)[0:26]
            if 'index' in parent_start:
                self.generate_header(node,"chapter")
            else:
                self.generate_header(node,"subsection")

    def generate_header(self,node,headertype):
        # Prepare and append Element
        title = node.next_node()
        header = ""
        

        if isinstance(title,nodes.title):
            title = title.astext()
            if headertype == "part":
                header = ("\\part*{%s}\n"
                          "\n") % (title)
            elif headertype == "chapter":
                command = title.replace(" ","")
                header = (
                    "\\newpage\n"
                    "\\chapter*{%s}\n"
                    "\\phantomsection"
                    "\\addcontentsline{toc}{chapter}"
                    "{\\protect \\normalsize \\textbf{--%s}}\n"
                    "\\singlespacing\n"
                    "\\textbf{"
                    "\\scriptsize\\%s}"
                    "\\vspace{2em} \n"
                    "\n \\noindent" ) % (title, title, command)
                
                self.current_chapter = title
                self.chapheader[title] = [title] 
            elif headertype == "section":
                header = "\\section*{%s}" % title
                self.chapheader[self.current_chapter].append(title)
            elif headertype == "subsection":
                header = "\\subsection*{%s}" % title
                self.chapheader[self.current_chapter].append(title)
            self.body.append(header)
        else:
            return SyntaxError(
                "This %s does not have a title."
                "That should not be possible..." % header) 



    def depart_section(self,node):
        pass

    def visit_document(self,node):
        #self.body.append(self.header.astext())
        start = []
        # Begin Document
        start.append("\\begin{document}\n")

        # Title Page
        start.append("\\begin{titlepage}\n"
                     
                     "\\begin{center}\n\n"
                     "\\HRuleFull\\par"
                     "\\vspace{5em}"
                     "\\bfseries \\Huge"
                     "\\textrm{\\ShowUpTitle}\\par"
                     "\n\n"
                     "\\vspace{8em}\\large\n"
                     "\\textrm{\\emph{\\ShowSubtitle}}\n\n"
                     "\\vspace{5em}\\Large\n"
                     "\\ShowAuthor\n"
                     "\\vspace{1.5em}\n"
                     "\\HRuleFull\n\n"
                     "\\end{center}\n"
                     "\\end{titlepage}\n")


        # Create Table of Contents
        start.append(""
                     "\\setcounter{tocdepth}{5}\n"
                     "\\tableofcontents \n")
        for i in start:
            self.body.append(i)


    def depart_document(self,node):
        self.header = BacchHeader(self.config,self.chapheader)
        self.body.insert(0,self.header.astext())
        self.body.append('\n\\end{document}\n')

    def visit_strong(self,node):
        self.body.append('\\textbf{')

    def depart_strong(self,node):
        self.body.append('}')

    def visit_emphasis(self,node):
        self.body.append('\emph{')

    def depart_emphasis(self,node):
        self.body.append('}')

    def visit_thought(self,node):
        self.body.append("\\thought{")

    def depart_thought(self,node):
        self.body.append("}")

    def visit_textsc(self,node):
        self.body.append("\\textsc{")

    def depart_textsc(self,node):
        self.body.append("}")

    def visit_line_block(self,node):
        if not self.config.bacch_doublespace_verse:
            self.body.append("\n\\begin{singlespace}")
        self.body.append('\n\\begin{verse}')

    def depart_line_block(self,node):
        self.body.append('\n\end{verse}')
        if not self.config.bacch_doublespace_verse:
            self.body.append("\\end{singlespace}\n")

    def visit_line(self,node):
        self.body.append('\n')

    def depart_line(self,node):
        """
        Requires two balckslashes after each line of verse,
        except for blank lines and lines preceding blank lines.
        """
        next_line = node.next_node(condition=nodes.line,siblings=1)
        if self.line_is_blank(node) and self.line_is_blank(next_line):
            self.body.append('\\\\')

    def line_is_blank(self,node):
        if not isinstance(node,nodes.line):
            return False
        else:
            return True if node.astext().strip() != '' else False

    def visit_block_quote(self,node):
        self.body.append('\n\\begin{quotation}')
    def depart_block_quote(self,node):
        self.body.append('\\end{quotation}\n')
                        
    def visit_synopsis(self,node):
        self.body.append('\n\\begin{synopsis}')
                      
    def depart_synopsis(self,node):
        self.body.append('\n\\end{synopsis}\n')

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
                


class BacchHeader(object):
    """
    Helper class that generates required LaTeX documentclass
    and other LaTeX header commands from conf.py for bacch.
    """
    header = []
    def __init__(self,config,chapheader):
        self.config = config
        self.chapheader = chapheader


    def astext(self):
        """
        Command to generate actual header text.  Called in translator
        during visit_document().
        """
        self.set_documentclass()
        self.set_command('title', self.config.bacch_title,required=True)
        self.set_command('runningtitle',self.config.bacch_runningtitle)
        self.set_command('author',self.config.bacch_author)
        self.set_command('authorname',self.config.bacch_authorname)
        #self.set_command('surname',self.config.bacch_surname)
        self.set_address()
        self.set_wordcount()
        self.set_command('frenchspacing',self.config.bacch_frenchspacing,typ=bool)
        self.set_command('disposable',self.config.bacch_disposable, typ=bool)
        self.header.append('\n')
        return '\n'.join(self.header)

    def set_documentclass(self):
        """
        Handles all options set for document class.
        """
        options = ['12pt','operight','pdftex']

        if self.config.bacch_nonsubmission:
            options.append('nonsubmission')
            if self.config.bacch_notitle:
                options.append('notitle')

        if self.config.bacch_novel:
            options.append('novel')

        sub_type = self.config.bacch_submission_type
        if sub_type:
            if sub_type in []:
                options.append(sub_type)
            else:
                raise ValueError("If present, bacch_submission_type must"
                                 "be set to ____.")

        quote_type = self.config.bacch_quote_type
        if quote_type:
            if quote_type in ['smart', 'dumb']:
                options.append(quote_type)
            else:
                raise ValueError("If present, bacch_quote_type must"
                                 "be set to 'smart' or 'dumb'.")

        if self.config.bacch_courier:
            options.append('courier')

        # Paper Sizes
        papersize = self.config.bacch_papersize
        if papersize == None:
            options.append('geometry')
            options.append('b5paper')
        elif papersize in ['a4paper', 'letterpaper','b4paper']:
            options.append('geometry')
            options.append(papersize)
        else:
            raise ValueError("If present, bacch_papersize must be set to"
                             "'a4paper' or 'letterpaper'.")

        options_str = ''
        if len(options) > 0:
            options_str = '[%s]' % (','.join(options))
        
        self.header.append('\\documentclass%s{%s}' % (options_str,'book'))
        
        base = ['\\usepackage{hyperref}\n',
                '\\usepackage[explicit, noindentafter]{titlesec}\n',
                "\\usepackage{titletoc}\n"
                "\\usepackage{fancyhdr}\n"
                "\\usepackage{setspace}\n"
                #"\\usepackage{showframe}\n"
            ]
        if self.config.bacch_submission_type == 'manuscript':
            base.append("\\usepackage["
                        "letterpaper"
                        "]{geometry} \n")
        else:
            base.append("\\usepackage["
                        "b5paper"
                        "]{geometry} \n")

        # Define Metadata
        title = self.config.bacch_title
        if title == None: title = "Untitled"
        base.append("\\newcommand{\\ShowTitle}{%s}\n" % title)
        base.append("\\newcommand{\\ShowUpTitle}{%s}\n" % title.upper())

        subtitle = self.config.bacch_subtitle
        if subtitle == None: subtitle = ""
        base.append("\\newcommand{\\ShowSubtitle}{%s}\n" % subtitle)

        surname = self.config.bacch_surname
        if surname == None: surname = ""
        base.append("\\newcommand{\\ShowSurname}{%s}\n" %surname)

        author = self.config.bacch_author
        if author == None: author = ''
        base.append("\\newcommand{\\ShowAuthor}{%s}\n" % author)

        # Page Style
        base.append("\\pagestyle{fancy}\n"
                    "\\fancyhead{}\n"
                    "\\fancyfoot{}\n")
        base.append("\\fancyfoot[RO,LE]{ \n"
                    "\\thepage"
                    "} \n")
        base.append("\\fancyhead[RO,LE]{ \n"
                    "\\tiny \\emph{\\ShowTitle} \\vspace{0.25em}\n"
                    "} \n")
        base.append("\\fancyhead[LE]{ \n"
                    "\\tiny \\ShowSurname \\vspace{0.25em}\n"
                    "} \n")
        #base.append("\\onehalfspacing\n")

        # LaTeX Commands
        base.append("\\newcommand{\\HRuleBreak}{ \n"
                    "\\rule{5em}{0.25mm}"
                    "}\n")
        base.append("\\newcommand{\\HRuleFull}{ \n"
                    "\\rule{\\linewidth}{0.5mm}"
                    "} \n")

        # Format Header
        base.append("\\titleclass{\\part}{page}\n"
                    "\\titleformat{\\part}\n"
                    "{\\Huge}{\\thepart}{}\n"
                    "{\\centering \\uppercase{\\textrm{\\textbf{#1}}}}\n"
                    "\n")

        base.append("\\titleclass{\\chapter}{straight}\n"
                    "\\titleformat{\\chapter}\n"
                    "{}{\\thechapter}{}{}\n"
                    "\\titlespacing{\\chapter}\n"
                    "{\\parindent}{\\baselineskip}{-2em}"
                    "\n")

        base.append("\\titleclass{\\section}{straight}\n"
                    "\\titleformat{\\section}\n"
                    "{}{\\thesection}{}{\\centering \\HRuleBreak} \n"
                    "\\titlespacing{\\section}\n"
                    "{\\parindent}{1em}{1em}"
                    "\n")
        base.append("\\titleclass{\\subsection}{straight}\n"
                    "\\titleformat{\\subsection}\n"
                    "{}{\\thesubsection}{}{} \n"
                    "\\titlespacing{\\subsection}\n"
                    "{\\parindent}{\\baselineskip}{-1em}"
                    "\n")
        for key in self.chapheader:
            command = self.generate_chaphead(key, self.chapheader[key])
            base.append(command)
                        
        for i in base:
            self.header.append(i)
    

    def generate_chaphead(self, header, titles):
        separator = ' -- '
        title = separator.join(titles) + "."
        header = header.replace(" ","")
        return "\\newcommand{\\%s}{%s} \n" % (header,title)


    def set_command(self,name,value,typ=str,required=False):
        """
        Handler for simple header commands.  String option \surname{Smith}.
        Boolean options \frenchspacing
        """
    
        if value and isinstance(value,typ):
            if isinstance(value,str):
                self.header.append('\\%s{%s}' % (name,value))
            elif isinstance(value,bool):
                self.header.append('\\%s' % name)
            elif required:
                raise ValueError("You must provide a valid %s in your conf.py"
                                 % name)
        
    def set_address(self):
        """
        Sets the address properly.
        """

        if not self.config.bacch_address:
            return

        address = self.config.bacch_address.splitlines()
        address_str = ''

        for i in range(0,len(address)):
            if (i < len(address) - 1):
                address[i] += '\\\\\n'
            address_str += address[i]

        self.header.appedn('\\address{%s}' % address_str)

    def set_wordcount(self):
        """
        Sets the wordcount, manually.  Turns off if set to None.
        """

        wc = self.config.bacch_wordcount
        if wc == None:
            self.header.append('\\wordcount{}')
        elif isinstance(wc,int):
            self.header.append('\\wordcount{%d}' % wc)





############################################
# General Functions and Classes
def add_nodes(app):
    # Suppress specific chapter numbering for specific chapters.
    # Make sure that we don't cause the default Sphinx builders
    # to failover when they encoutner an unknown node.

    app.add_node(suppress_numbering,html=(skip_me,None),latex=(skip_me,None),
                 text = (skip_me,None),man = (skip_me,None))
    app.add_directive('suppress_numbering', BacchSuppressNumberingDirective)

    # Allow the user to ad a synopsis section anywhere in doc.
    app.add_node(synopsis, 
                 html=(pass_me,pass_me),
                 latex = (pass_me,pass_me),
                 text = (pass_me, pass_me),
                 man = (pass_me,pass_me))
    app.add_directive('suppress_synopsis', BacchSynopsisDirective)

    # Add two inline styles thought and textsc
    app.add_node(thought,
                 html = (pass_me, pass_me),
                 latex = (pass_me,pass_me),
                 man = (pass_me,pass_me))
    app.add_generic_role('thought',thought)

    app.add_node(textsc,
                 html = (pass_me,pass_me),
                 latex = (pass_me, pass_me),
                 man = (pass_me, pass_me))
    app.add_generic_role('textsc',textsc)

def skip_me(node):
    raise nodes.SkipNode

def pass_me(node):
    pass

class thought(nodes.Inline,nodes.TextElement):
    pass

class textsc(nodes.Inline, nodes.TextElement):
    pass

class suppress_numbering(nodes.General, nodes.Element):
    pass

class synopsis(nodes.Structural, nodes.Element):
    pass

class BacchSuppressNumberingDirective(Directive):
    def run(self):
        return [ suppress_numbering('') ]

class BacchSynopsisDirective(Directive):
    
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






#####################################
# bacch Special Builder setup
def setup(app):
    print("Initialized bacch Builder extension")
    app.add_builder(BacchBuilder)

    # Add custom nodes, roles and directives
    add_nodes(app)

    # REQUIRED: Sets book title.
    app.add_config_value('bacch_title', None, '')

    # REQUIRED: Sets the author name.
    app.add_config_value('bacch_author', None, '')

    # Change the layout, opens 'notitle' option.
    app.add_config_value('bacch_nonsubmission', False, '')
    app.add_config_value('bacch_notitle', False, '')

    # Use chapters, switch to novel layout
    app.add_config_value('bacch_novel', False,'')

    # Tweak Layout
    app.add_config_value('bacch_submission_type',None,'')

    # Change Quote Behavior
    app.add_config_value('bacch_quote_type', None,'')
    
    # Override default monospace font
    app.add_config_value('bacch_courier', False,'')
    
    # Change Papersize
    app.add_config_value('bacch_papersize',None,'')

    # Change Scene Separator from '#'
    app.add_config_value('bacch_sceneseparator', None, '')

    # Chnage end of story symbol from '# # # # #'
    app.add_config_value('bacch_thirty', None, '')
    
    # Override running header wiht arbitrary LaTeX
    app.add_config_value('bacch_msheading', None, '')

    # Set title in running header, overriding the title
    app.add_config_value('bacch_runningtitle', None, '')

    # Set subtitle
    app.add_config_value('bacch_subtitle',None,'')

    # Set real name
    app.add_config_value('bacch_authorname', None, '')

    # Set name in running header
    app.add_config_value('bacch_surname', None, '')

    # Freeform multiline address
    app.add_config_value('bacch_address', None, '')

    # Define Wordcount manually
    app.add_config_value('bacch_wordcount','default','')

    # Mark Document as Disposable
    app.add_config_value('bacch_disposable',False,'')

    #Change to one space between sentences.
    app.add_config_value('bacch_frenchspacing',False,'')

    # Doublespace versus single-spacing
    app.add_config_value('bacch_doublespace_verse',False,'')

    # Whether you want to include parts
    app.add_config_value('bacch_include_parts',False,'')

    # Definte Chapter header separate
    app.add_config_value('bacch_chap_sep',None, '')


