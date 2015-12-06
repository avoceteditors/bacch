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

from writers.pdftranslator import PDFTranslator
from writers.odftranslator import ODFTranslator

########################################
# Writer Class
class BaseWriter(docutils.writers.Writer):

    def __init__(self, config):
        docutils.writers.Writer.__init__(self)
        self.config = self.configure_defaults(config)

    def translate(self):
        translator = BaseTranslator(self.document, self.config)
        self.document.walkabout(translator)
        self.output = translator.return_text()

        
    def configure_defaults(self, config):

        self.bacch_chapter = {
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

        self.gnomon_chapter = {
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
        
        self.bacch_section = {
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
        
        self.gnomon_section = {
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

        self.bacch_subsection = {
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

        self.gnomon_subsection = {
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

        self.bacch_subsubsection = {
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

        self.gnomon_subsubsection = {
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

        self.bacch_paragraph = {
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

        self.gnomon_paragraph = {
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

        
        self.bacch_subparagraph = {
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

        self.gnomon_subparagraph = {
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

        self.bacch_header = {
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

        self.gnomon_header = {
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
        
        
        format_list = ['chapter', 'section', 'subsection',
                       'subsubsection', 'paragraph', 'subparagraph',
                       'header']
        builder_list = ['bacch', 'gnomon']

        for builder in builder_list:
            for section in format_list:
                call = '%s_%s' % (builder, section)
                config_call = '%s_format' % call
                default_values = getattr(self, call)
                config_values = getattr(config, config_call)
                
                base = set_default(config_values, default_values)
                setattr(config, config_call, base)
        return config
                
def set_default(configbase, default):
    base = {}
    for key in default:
        try:
            base[key] = configbase[key]
        except:
            base[key] = default[key]
    return base


                                      

        



        
####################################
# Translator
class BaseTranslator(nodes.NodeVisitor):

    def __init__(self, document, config):
        nodes.NodeVisitor.__init__(self, document)
        self.config = config
        build_type = self.config.bacch_build_type
        
        writer_type = getattr(self.config, '%s_output_type' % build_type)
        if writer_type == 'pdf':
            self.formatter = PDFTranslator(self.config)
        elif writer_type == 'odf':
            self.formatter = ODFTranslator(self.config)
        else:
            raise ValueError("Error: %s is an invalid output format."
                             "\n" % writer_type)    

        self.assign_node_handlers()

    

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

            if name[1] == "skip":

                setattr(self, 'visit_%s' % name[0],
                        skip_node)
            elif name[1] == "pass":
                setattr(self, 'visit_%s' % name[0],
                        pass_node)
                setattr(self, 'depart_%s' % name[0],
                        pass_node)
            else:
                raise ValueError("Error Node Handler:"
                                 "%s neither skip nor pass" % name[0])


    def visit_Text(self, node):
        self.formatter.visit_Text(node)

    def depart_Text(self, node):
        self.formatter.depart_Text(node)

    def visit_document(self, node):
        self.formatter.visit_document(node)

    def depart_document(self, node):
        self.formatter.depart_document(node)

    def visit_paragraph(self, node):
        self.formatter.visit_paragraph(node)

    def depart_paragraph(self, node):
        self.formatter.depart_paragraph(node)
        
    def visit_section(self, node):
        self.formatter.visit_section(node)

    def depart_section(self, node):
        self.formatter.depart_section(node)

    def visit_strong(self, node):
        self.formatter.visit_strong(node)

    def depart_strong(self, node):
        self.formatter.depart_strong(node)
        
    def visit_emphasis(self, node):
        self.formatter.visit_emphasis(node)

    def depart_emphasis(self, node):
        self.formatter.depart_emphasis(node)

    def visit_literal(self, node):
        self.formatter.visit_literal(node)

    def depart_literal(self, node):
        self.formatter.depart_literal(node)


    def visit_literal_emphasis(self, node):
        self.formatter.visit_literal_emphasis(node)

    def depart_literal_emphasis(self, node):
        self.formatter.depart_literal_emphasis(node)

    # Parse Notes
    def visit_note(self, node):
        self.formatter.visit_note(node)
        
    def depart_note(self, node):
        self.formatter.depart_note(node)
            

    def return_text(self):
        return self.formatter.return_text()
        
#########################
# General Functions
def skip_node(node):
    raise nodes.SkipNode
def pass_node(node):
    pass
