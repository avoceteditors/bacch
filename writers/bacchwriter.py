#!/usr/bin/env python3


############################
# Module Imports

import codecs, os.path, re, subprocess

from sphinx.builders import Builder
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.compat import Directive

from docutils import nodes
import docutils.writers
from docutils.io import StringOutput
import roman

from writers.bacchheader import BacchHeader


############################
# Writer Class
class BacchWriter(docutils.writers.Writer):

    def __init__(self, config, build):
        docutils.writers.Writer.__init__(self)
        self.config = config
        self.config.bacch_build_type = build

    def translate(self):
        translator = BacchTranslator(self.document, self.config)
        self.document.walkabout(translator)
        self.output = translator.astext()



############################
# Translation Class
class BacchTranslator(nodes.NodeVisitor):

    # Initialize Class
    def __init__(self, document, config):
        nodes.NodeVisitor.__init__(self, document)
        self.config = config

        build = self.config.bacch_build_type
        if build == "bacch":
            self.level = 0
        elif build == "gnomon":
            self.level = 2
            
        self.body = []

        self.chapter_count = 0

        # Configure Default Format
        self.format_defaults()
        
        # Parse Nodes
        self.assign_node_handlers()


    # Return Text
    def astext(self):
        return ''.join(self.body)

    # Format Defaults
    def format_defaults(self):
        b_chapter = {
            "name": "chapter",
            "class": "top",
            "format_shape": '',
            "format_format": '',
            "format_label": '\\thechapter',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '\\parindent',
            "spacing_before_sep": '\\baselineskip',
            "spacing_after_sep": '0em',
            "spacing_right": '',
            "contents_use": True,
            "contents_left": '1em',
            "contents_above": '\\protect \\small',
            "contents_label_width":'1em',
            "contents_leader_width":'1em',
            "title_use": True,
            "title_prefix": ('\\begin{center}'
                             '\\vspace{4em} \\Large'
                             '\\makebox[\\linewidth][s]{'
                             '\\bfseries \\MakeTextUppercase{'
            ),
            "title_suffix": '}} \\end{center}',
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.bacch_chapter_format = self.set_format(
            self.config.bacch_chapter_format, b_chapter)
        
        b_section = {
            "name": "section",
            "class": "top",
            "format_shape": '',
            "format_format": '',
            "format_label": '\\thesection',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '\\parindent',
            "spacing_before_sep": '\\baselineskip',
            "spacing_after_sep": '0em',
            "spacing_right": '',
            "contents_use": True,
            "contents_left": '2em',
            "contents_above":'\\protect \\small',
            "contents_label_width":'1em',
            "contents_leader_width":'1em',
            "title_use": True,
            "title_prefix": ('\\begin{center}'
                             '\\textls[650]{'
                             '\\scshape'
            ),
            "title_suffix": ('}\\par\\vspace{10em}\\end{center}\n\n'),
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.bacch_section_format = self.set_format(
            self.config.bacch_section_format, b_section)

        b_subsection = {
            "name": "subsection",
            "class": "straight",
            "format_shape": '',
            "format_format": '',
            "format_label": '\\thesubsection',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '\\parindent',
            "spacing_before_sep": '1em',
            "spacing_after_sep": '1em',
            "spacing_right": '',
            "contents_use": False,
            "contents_left": '',
            "contents_above":'',
            "contents_label_width":'',
            "contents_leader_width":'',
            "title_use": False,
            "title_prefix": '',
            "title_suffix": '',
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.bacch_subsection_format = self.set_format(
            self.config.bacch_subsection_format, b_subsection)

        b_subsubsection = {
            "name": "subsubsection",
            "class": "straight",
            "format_shape": '',
            "format_format": '',
            "format_label": '\\thesubsubsection',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '\\parindent',
            "spacing_before_sep": '\\baselineskip',
            "spacing_after_sep": '-1em',
            "spacing_right": '',
            "contents_use": False,
            "contents_left": '',
            "contents_above":'',
            "contents_label_width":'',
            "contents_leader_width":'',
            "title_use": False,
            "title_prefix": '',
            "title_suffix": '',
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.bacch_subsubsection_format = self.set_format(
            self.config.bacch_subsubsection_format, b_subsubsection)

        b_paragraph = {
            "name": "paragraph",
            "class": "straight",
            "format_shape": '',
            "format_format": '',
            "format_label": '',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '',
            "spacing_before_sep": '',
            "spacing_after_sep": '',
            "spacing_right": '',
            "contents_use": False,
            "contents_left": '',
            "contents_above":'',
            "contents_label_width":'',
            "contents_leader_width":'',
            "title_use": False,
            "title_prefix": '',
            "title_suffix": '',
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.bacch_paragraph_format = self.set_format(
            self.config.bacch_paragraph_format, b_paragraph)

        b_subparagraph = {
            "name": "subparagraph",
            "class": "straight",
            "format_shape": '',
            "format_format": '',
            "format_label": '',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '',
            "spacing_before_sep": '',
            "spacing_after_sep": '',
            "spacing_right": '',
            "contents_use": False,
            "contents_left": '',
            "contents_above":'',
            "contents_label_width":'',
            "contents_leader_width":'',
            "title_use": False,
            "title_prefix": '',
            "title_suffix": '',
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.bacch_subparagraph_format = self.set_format(
            self.config.bacch_subparagraph_format, b_subparagraph)

        b_header = {
            "headrulewidth": "0pt",
            "footrulewidth": "0pt",
            "format_head_LE": "\\small \\vspace{0.25in}",
            "format_head_RO": "\\small \\vspace{0.25in}",
            "format_head_CE": ' ',
            "format_head_CO": ' ',
            "format_head_LO": ' ',
            "format_head_RE": ' ',
            "format_foot_LE": "\\small \\thepage \\vspace{0.25in}",
            "format_foot_RO": "\\small \\thepage \\vspace{0.25in}",
            "format_foot_CE": ' ',
            "format_foot_CO": ' ',
            "format_foot_LO": ' ',
            "format_foot_RE": ' ',
            
            }
        self.config.bacch_header_format = self.set_format(
            self.config.bacch_header_format, b_header)


        ###############################
        # Define Gnomon Fomrats
        g_chapter = {
            "name": "chapter",
            "class": "top",
            "format_shape": '',
            "format_format": '',
            "format_label": '\\thechapter',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '\\parindent',
            "spacing_before_sep": '\\baselineskip',
            "spacing_after_sep": '0em',
            "spacing_right": '',
            "contents_use": True,
            "contents_left": '1em',
            "contents_above": '\\protect \\small',
            "contents_label_width":'1em',
            "contents_leader_width":'1em',
            "title_use": True,
            "title_prefix": ('\\begin{center}'
                             '\\vspace{4em} \\Large'
                             '\\makebox[\\linewidth][s]{'
                             '\\bfseries \\MakeTextUppercase{'
            ),
            "title_suffix": '}} \\end{center}',
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.gnomon_chapter_format = self.set_format(
            self.config.gnomon_chapter_format, g_chapter)

        g_section = {
            "name": "section",
            "class": "straight",
            "format_shape": '',
            "format_format": '',
            "format_label": '\\thesection',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '\\parindent',
            "spacing_before_sep": '\\baselineskip',
            "spacing_after_sep": '0em',
            "spacing_right": '',
            "contents_use": True,
            "contents_left": '2em',
            "contents_above":'\\protect \\small',
            "contents_label_width":'1em',
            "contents_leader_width":'1em',
            "title_use": False,
            "title_prefix": ('\\begin{center}'
                             '\\textls[650]{'
                             '\\scshape'
            ),
            "title_suffix": ('}\\par\\vspace{10em}\\end{center}\n\n'),
            "title_alternative": '',
            "par_noindent": True
        }

        self.config.gnomon_section_format = self.set_format(
            self.config.gnomon_section_format, g_section)

        g_subsection = {
            "name": "subsection",
            "class": "straight",
            "format_shape": '',
            "format_format": '',
            "format_label": '\\thesubsection',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '\\parindent',
            "spacing_before_sep": '1em',
            "spacing_after_sep": '1em',
            "spacing_right": '',
            "contents_use": False,
            "contents_left": '',
            "contents_above":'',
            "contents_label_width":'',
            "contents_leader_width":'',
            "title_use": False,
            "title_prefix": '',
            "title_suffix": '',
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.gnomon_subsection_format = self.set_format(
            self.config.gnomon_subsection_format, g_subsection)

        g_subsubsection = {
            "name": "subsubsection",
            "class": "straight",
            "format_shape": '',
            "format_format": '',
            "format_label": '\\thesubsubsection',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '\\parindent',
            "spacing_before_sep": '\\baselineskip',
            "spacing_after_sep": '-1em',
            "spacing_right": '',
            "contents_use": False,
            "contents_left": '',
            "contents_above":'',
            "contents_label_width":'',
            "contents_leader_width":'',
            "title_use": False,
            "title_prefix": '',
            "title_suffix": '',
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.gnomon_subsubsection_format = self.set_format(
            self.config.gnomon_subsubsection_format, g_subsubsection)

        g_paragraph = {
            "name": "paragraph",
            "class": "straight",
            "format_shape": '',
            "format_format": '',
            "format_label": '',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '',
            "spacing_before_sep": '',
            "spacing_after_sep": '',
            "spacing_right": '',
            "contents_use": False,
            "contents_left": '',
            "contents_above":'',
            "contents_label_width":'',
            "contents_leader_width":'',
            "title_use": False,
            "title_prefix": '',
            "title_suffix": '',
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.gnomon_paragraph_format = self.set_format(
            self.config.gnomon_paragraph_format, g_paragraph)

        g_subparagraph = {
            "name": "subparagraph",
            "class": "straight",
            "format_shape": '',
            "format_format": '',
            "format_label": '',
            "format_sep": '',
            "format_before": '',
            "format_after": '',
            "spacing_left": '',
            "spacing_before_sep": '',
            "spacing_after_sep": '',
            "spacing_right": '',
            "contents_use": False,
            "contents_left": '',
            "contents_above":'',
            "contents_label_width":'',
            "contents_leader_width":'',
            "title_use": False,
            "title_prefix": '',
            "title_suffix": '',
            "title_alternative": '',
            "par_noindent": True
        }
        self.config.gnomon_subparagraph_format = self.set_format(
            self.config.gnomon_subparagraph_format, g_subparagraph)

        g_header = {
            "headrulewidth": "0pt",
            "footrulewidth": "0pt",
            "format_head_LE": ("\\small \\vspace{0.25in}"
                               "\\emph{\\showtitle}"),
            "format_head_RO": ("\\small \\vspace{0.25in}"
                               "\\showsectitle"),
            "format_head_CE": ' ',
            "format_head_CO": ' ',
            "format_head_LO": ' ',
            "format_head_RE": ' ',
            "format_foot_LE": "\\small \\thepage \\vspace{0.5em}",
            "format_foot_RO": "\\small \\thepage \\vspace{0.5em}",
            "format_foot_CE": ' ',
            "format_foot_CO": ' ',
            "format_foot_LO": ' ',
            "format_foot_RE": ' ',
            
            }
        self.config.gnomon_header_format = self.set_format(
            self.config.gnomon_header_format, g_header)
   

        
    def set_format(self, parameter, default):
        base = {}
        for key in default:
            try:
                 base[key] = parameter[key]
            except:
                base[key] = default[key]
        return base
            
            
    # Node Handlers
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
            ('inline', 'pass'),
            ('label', 'skip'),
            ('legend', 'skip'),
            ('list_item', 'skip'),
            ('literal', 'pass'),
            ('literal_block', 'skip'),
            ('literal_emphasis', 'skip'),
            ('literal_inline','pass'),
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
            ('toctree','skip'),
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
                raise ValueError("When assigning node handlers."
                                 "you must set %s to either "
                                 "'skip' or 'pass'." % name[0])

    ################################
    # Parse Text
    def visit_Text(self, node):
        reserved_latex_chars = '["{}\\\^&\%\$#~_]'
        text = re.sub(reserved_latex_chars,
                    self.escaped_chars,
                    node.astext())
        self.body.append(text)

    def depart_Text(self, node):
        pass

    ################################
    # Escape LaTeX Characters
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

    ################################
    # Parse Paragraphs
    def visit_paragraph(self, node):
        self.body.append('\n')

    def depart_paragraph(self, node):
        self.open_quotes = False
        self.body.append('\n')


    #################################
    # Parse Section
    def visit_section(self, node):
        self.level += 1
        title = node.next_node().astext()
        text = ''
        
        if self.level == 2:
            text = self.gen_sect("chapter", title,
                                 self.config.bacch_chapter_format)
        elif self.level == 3:
            text = self.gen_sect("section", title,
                                 self.config.bacch_section_format)
        elif self.level == 4:
            text = self.gen_sect("subsection", title,
                                 self.config.bacch_subsection_format)
        elif self.level == 5:
            text = self.gen_sect("subsubsection", title,
                                 self.config.bacch_subsubsection_format)
        elif self.level == 6:
            text = self.gen_sect("paragraph", title,
                                 self.config.bacch_paragraph_format)
        elif self.level == 7:
            text = self.gen_sect("subparagraph", title,
                                 self.config.bacch_subparagraph_format)

        self.body.append(text)

    def depart_section(self, node):
        self.level += -1


    # Generate Chapter Header

    # Generate Section Headers
    def gen_sect(self, kind, title, sect_config):
        base = "\\%s*{%s}\n\n" % (kind, title)
        if sect_config["contents_use"]:
            base = base + ("\\phantomsection\n"
                    "\\addcontentsline{toc}{%s}"
                    "{%s %s}\n"
            ) % (kind, sect_config["contents_above"], title)
            
        # Parse Titles
        head = ''
        build_type = self.config.bacch_build_type
        settings = getattr(self.config, '%s_%s_format' % (build_type, kind))

        if settings["title_use"]:
            head = '\n'.join([settings["title_prefix"],
                             title,
                             settings["title_suffix"]])
        else:
            head = settings["title_alternative"]

        if settings["par_noindent"]:
            head += '\n\n\\noindent'
        if build_type == "gnomon" and kind == "section":
            self.config.section_title = title

        base += head
        return base



    ###########################
    # Parse Document

    def visit_document(self, node):

        base = ["\\begin{document}\n"]

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
        self.body.append(docstart)

    def depart_document(self, node):
        
        header = BacchHeader(self.config)
        self.body.insert(0, header.astext())
        self.body.append('\n\n\\end{document}')


    # Formatting Options
    def visit_strong(self, node):
        self.body.append('\\textbf{')

    def depart_strong(self, node):
        self.body.append('}')

    def visit_emphasis(self, node):
        self.body.append('\\emph{')

    def depart_emphasis(self, node):
        self.body.append('}')

    def visit_literal(self, node):
        self.body.append('\\textbf{')

    def depart_literal(self, node):
        self.body.append('}')

    def visit_literal_emphasis(self, node):
        self.body.append('\\emph{')

    def depart_literal_emphasis(self, node):
        self.body.append('}')

    # Parse Notes
    def visit_note(self, node):
        self.body.append('\\begin{framed}'
                        '\\small \\noindent')

    def depart_note(self, node):
        self.body.append('\\end{framed}\n')




#################################################
# Skip and Pass Functions for parsing documents
def skip_me(node):
    raise nodes.SkipNode

def pass_me(node):
    pass
