#! /usr/bin/env python3

###############################################
# Module Imports
import codecs, os.path, re
from docutils.io import StringOutput

from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees

from docutils import nodes
from addnodes import skip_me, pass_me, suppress_numbering
from docutils import nodes, writers
from sphinx.addnodes import start_of_file
from sphinx.util.compat import Directive


##################################################
# BookBuilder Class
class Bookbuilder(Builder):
    name = "bacch-book"
    format = "latex"
    out_suffix = ".tex"
    writer = None
    
    # TODO grab initial bacch configuration
    def init(self):
        pass
    
    def get_outdated_docs(self):
        return 'all documents'
    
    def prepare_writing(self, docnames):
        self.writer = BookWriter(self.config)
    
    def get_relative_uri(self, from_, to, typ=None):
        return self.get_target_uri(to, typ)
    
    # LaTeXBuilder has slightly more complicated behavior here, might need to copy wholesale    
    def get_target_uri(self, docname, typ):
        return '%' + docname

    # Overriding the default write() implementation because we must write to
    # a single file in TOC order. So rather than getting write_doc() called for us
    # multiple times, we assemble one big inline doctree and call write_doc() once.
    # 
    # Code adapted from SinglePageHTML, since that seems to be the simplest implementation.
    def write(self, *ignored):
        docnames = self.env.all_docs

        self.info(bold('Preparing documents...'), nonl=True)
        self.prepare_writing(docnames)
        self.info('Done')

        self.info(bold('Assembling single document... '), nonl=True)
        doctree = self.assemble_doctree()
        self.info('Done')
        self.info()
        self.info(bold('Writing... '), nonl=True)
        self.write_doc(self.config.master_doc, doctree)
        outfile = path.join(self.outdir, os_path(self.config.master_doc) + self.out_suffix)
        ensuredir(path.dirname(outfile))
        self.write_file(outfile, self.writer.output)
        self.info('Done')
        
    def assemble_doctree(self):
        master = self.config.master_doc
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set() , master, tree, darkgreen)
        tree['docname'] = master
        
        # skip code that checks references, etc.
        return tree
    
    def write_doc(self, docname, doctree):
        destination = StringOutput(encoding='utf-8')
        output = self.writer.write(doctree, destination)
    
    def finish(self):
        self.info(bold('Copying Makefile... '), nonl=True)
        outfile = path.join(self.outdir, 'Makefile')
        self.write_file(outfile, makefile_sffms)
        self.info('done')
    
    def write_file(self, outfile, content):
        try:
            f = codecs.open(outfile, 'w', 'utf-8')
            try:
                f.write(content)
            finally:
                f.close()
        except (IOError, OSError), err:
            self.warn("Error writing file %s: %s" % (outfile, err))


############################
# Writer Classes
class BookWriter(writers.Writer):
    output = None
    document = None

    def __init__(self, config):
        writers.Writer.__init__(self)
        self.config = config

    def translate(self):
        translator = BookTranslator(self.document, self.config)
        self.document.walkabout(translator)
        self.output = translator.astext()

class BookTranslator(nodes.NodeVisitor):
    body = []
    
    def __init__(self, document, config):
        nodes.NodeVisitor.__init__(self, document)
        self.config = config
        self.header = BookHeader(config)
        self.assign_node_handlers()

    def astext(self):
        return ''.join(self.body)
    
    def visit_Text(self, node):
        reserved_latex_chars = '[{}\\\^&\%\$#~_]'
        text = re.sub(reserved_latex_chars, self.escaped_chars, node.astext())
        self.body.append(text)
    
    def escaped_chars(self, match):
        if match.group(0) == '~':
            return '$\\sim$'
        elif match.group(0) == '\\':
            return '$\\backslash$'
        elif match.group(0) == '^':
            return '\\^{}'
        else:
            return '\\' + match.group(0)

    def depart_Text(self, node): 
        pass
        
    def visit_paragraph(self, node):
        self.body.append('\n')
        
    def depart_paragraph(self, node):
        self.body.append('\n')
    
    def visit_section(self, node):
        """
        Logic to determine whether to treat as new chapter, new scene,
        or nothing.
        """
      
        # We do not actually want to emit a new scene or chapter for
        # the top-level section.
        if self.is_toplevel_section(node):
            pass
        elif self.is_new_chapter(node):
            self.body.append(self.new_chapter(node))
        else:
            self.body.append('\n\\newscene\n')
            

    def is_toplevel_section(self, node):
        ''' 
        If you are a section, and parent is a document with a 
        'docname' attribute, you are the top-level section 
        (unless the source markup is very malformed).
        '''
        if isinstance(node.parent, nodes.document) and 'docname' in node.parent:
            return True
        else:
            return False
    

    def is_new_chapter(self, node):
        '''
        Determines whether a section is a new chapter. Chapters are 
        only relevant for novels. The logic is slightly different 
        depending on whether the novel is single-file or multi-file.
        '''
        if self.config.bacch_novel:
            # a multi-file novel with a toctree directive
            if isinstance(node.parent, nodes.document):
                return True
            # a single-file novel with chapters correctly nested under 
            #  the top-level section
            elif isinstance(node.parent.parent, nodes.document) and 'docname' in node.parent.parent:
                return True
        else:
            return False



    def new_chapter(self, node):
        sn = node.next_node(condition=suppress_numbering)
        if isinstance(sn, suppress_numbering) and sn.parent is node:
            sn = '*'
        else:
            sn = ''
            
        title = node.next_node()
        if isinstance(title, nodes.title):
            return '\n\chapter' + sn + '{' + title.astext() + '}\n'
        else:
            raise SyntaxError("This chapter does not seem to have a title. That shouldn't be possible...")


    def depart_section(self, node): 
        pass
    
    def visit_document(self, node):
        self.body.append(self.header.astext())
        self.body.append('\\begin{document}\n')
    
    def depart_document(self, node):
        self.body.append('\n\\end{document}\n')
    
    def visit_strong(self, node):
        self.body.append('\\textbf{')
    
    def depart_strong(self, node):
        self.body.append('}')
    
    def visit_emphasis(self, node):
        self.body.append('\emph{')
       
    def depart_emphasis(self, node):
        self.body.append('}')
    
    def visit_thought(self, node):
        self.body.append('\\thought{')
        
    def depart_thought(self, node):
        self.body.append('}')
    
    def visit_textsc(self, node):
        self.body.append('\\textsc{')

    def depart_textsc(self, node):
        self.body.append('}')
 
    def visit_line_block(self, node):
        if not self.config.bacch_doublespace_verse:
            self.body.append('\n\\begin{singlespace}')
        self.body.append('\n\\begin{verse}')
         
    def depart_line_block(self, node):
        self.body.append('\n\end{verse}\n')
        if not self.config.bacch_doublespace_verse:
            self.body.append('\\end{singlespace}\n')

    def visit_line(self, node):
        self.body.append('\n')

        
    def depart_line(self, node):
        '''
        Sffms requires us to insert two backslashes after each 
        line of verse, *except* for blank lines and lines 
        preceding blank lines.
        '''
        next_line = node.next_node(condition=nodes.line, siblings=1)
        if self.line_is_blank(node) and self.line_is_blank(next_line):
            self.body.append('\\\\')

    def line_is_blank(self, node):
        if not isinstance(node, nodes.line):
            return False
        else:
            return True if node.astext().strip() != '' else False
        
    def visit_block_quote(self, node):
        self.body.append('\n\\begin{quotation}')
        
    def depart_block_quote(self, node):
        self.body.append('\end{quotation}\n')
    
    def visit_synopsis(self, node):
        self.body.append('\n\\begin{synopsis}')
        
    def depart_synopsis(self, node):
        self.body.append('\\end{synopsis}\n')
        
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
                setattr(self, 'visit_'+name[0], skip_me)
            elif name[1] == 'pass':
                setattr(self, 'visit_'+name[0], pass_me)
                setattr(self, 'depart_'+name[0], pass_me)
            else:
                raise ValueError(
                    "When assigning node handlers, you must set %s to either 'skip' or 'pass'." % name[0])
    

##########################################
# Defines BookHeader 
class BookHeader(object):
    """
    A helper class that uses bacch config values to 
    generate the required LaTeX documentclass and other 
    LaTeX header commands. 
    """
    header = []
    
    def __init__(self, config):
        self.config = config
    
    def astext(self):
        """
        The command for generating the actual header text. 
        Called in the translator during visit_document() 
        (since after inlining the tree, there is only one document).
        """
      self.set_documentclass()
        self.set_command('title', self.config.bacch_title, required=True)
        self.set_command('runningtitle', self.config.bacch_runningtitle)
        self.set_command('author', self.config.bacch_author, required=True)
        self.set_command('authorname', self.config.bacch_authorname)
        self.set_command('surname', self.config.bacch_surname)
        self.set_address()
        self.set_wordcount()
        self.set_command('frenchspacing', self.config.bacch_frenchspacing, typ=bool)
        self.set_command('disposable', self.config.bacch_disposable, typ=bool)
        self.set_command('sceneseparator', self.config.bacch_sceneseparator)
        self.set_command('thirty', self.config.bacch_thirty)
        self.set_command('msheading', self.config.bacch_msheading)
        self.header.append('\n')
        return '\n'.join(self.header)

    def set_documentclass(self):
        r"""
        Handles all options [x,y,z] set for the document class. 
        Output resembles::

          \documentclass[novel,baen]{sffms}
        
        This function enforces various restrictions on which options are allowed.
        """
        options = []

        if self.config.bacch_nonsubmission:
            options.append('nonsubmission')
            if self.config.bacch_notitle:
                options.append('notitle') 
        
        if self.config.bacch_novel:
            options.append('novel')

        sub_type = self.config.bacch_submission_type
        if sub_type: 
            if sub_type in ['anon', 'baen', 'daw', 'wotf']:
                options.append(sub_type)
            else:
                raise ValueError("If present, bacch_submission_type must be set to 'anon', 'baen', 'daw', or 'wotf'.")
                
        quote_type = self.config.bacch_quote_type
        if quote_type:
            if quote_type in ['smart', 'dumb']:
                options.append(quote_type)
            else:
                raise ValueError("If present, bacch_quote_type must be set to 'smart' or 'dumb'.")
   
        if self.config.bacch_courier:
            options.append('courier')
        
        # despite what the sffms LaTeX docs imply, I don't think sffms supports any other paper sizes.
        papersize = self.config.bacch_papersize
        if papersize == None:
            pass
        elif papersize in ['a4paper', 'letterpaper']:
            options.append('geometry')
            options.append(papersize)
        else:
            raise ValueError("If present, bacch_papersize must be set to 'a4paper' or 'letterpaper'.")
        
        options_str = ''
        if len(options) > 0:
            options_str = '[' + ','.join(options) + ']'
           
        self.header.append('\\documentclass' + options_str + '{sffms}')

    def set_command(self, name, value, typ=str, required=False):
        r"""
        Handles all simple header commands: string and 
        boolean, required and optional. A string option resembles::
        
          \surname{Smith}
        
        A boolean option resembles::
        
          \frenchspacing
        """
        if value and isinstance(value, typ):
            if isinstance(value, str):
                self.header.append('\\' + name + '{' + value + '}')
            elif isinstance(value, bool):
                self.header.append('\\' + name)
        elif required:
            raise ValueError("You must provide a valid %s in your conf.py." % name)
    
   
    def set_address(self):
        """
        Sets the address properly. The address requires some 
        funky logic where we need to add a LaTeX newline (two 
        backslashes) after each line, *except* for the last line.
        """
        if not self.config.bacch_address:
            return

        address = self.config.bacch_address.splitlines()
        address_str = ''
        
        for i in range(0, len(address)):
            if (i < len(address) - 1): 
                address[i] += '\\\\\n'
            address_str += address[i]
            
        self.header.append('\\address{' + address_str + '}')


    def set_wordcount(self):
        """
        Sets the wordcount manually to a value (if set to a number) or turns off 
        the wordcount entirely (if set to None).
        """
        wc = self.config.bacch_wordcount
        if wc == None:
            self.header.append('\\wordcount{}')
        elif isinstance(wc, int):
            self.header.append('\\wordcount{%d}' % wc )

class thought(nodes.Inline, nodes.TextElement): 
    pass

class textsc(nodes.Inline, nodes.TextElement): 
    pass

class suppress_numbering(nodes.General, nodes.Element): 
    pass
    
class synopsis(nodes.Structural, nodes.Element): 
    pass


class BookSuppressNumberingDirective(Directive):
    def run(self):
        return [suppress_numbering('')]

class BookSynopsisDirective(Directive):
    
    node_class = synopsis
    has_content = True
    
    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        synopsis_node = self.node_class(rawsource=text)
        self.state.nested_parse(self.content, self.content_offset, synopsis_node)
        return [synopsis_node]



##############################################
# Add Nodes Functions and classes
def add_nodes(app):    
    # Suppress specific chapter numbering for specific 
    #  chapters. Make sure that we don't make the default 
    #  Sphinx builders fall over when they encounter an unknown node.
    app.add_node(suppress_numbering, html=(skip_me, None), latex=(skip_me, None),
        text=(skip_me, None), man=(skip_me, None))
    app.add_directive('suppress_numbering', BookSuppressNumberingDirective)
    
    # Allow the user to add a synopsis section anywhere in 
    #  the document. Pass it through to the default Sphinx 
    #  builders and hope it looks okay.
    app.add_node(synopsis, html=(pass_me, pass_me), latex=(pass_me, pass_me),
        text=(pass_me, pass_me), man=(pass_me, pass_me))
    app.add_directive('synopsis', BookSynopsisDirective)
    
    # Add two inline styles defined by sffms (thought and textsc)
    app.add_node(thought, html=(pass_me, pass_me), latex=(pass_me, pass_me),
        text=(pass_me, pass_me), man=(pass_me, pass_me))
    app.add_generic_role('thought', thought)
    
    app.add_node(textsc, html=(pass_me, pass_me), latex=(pass_me, pass_me),
        text=(pass_me, pass_me), man=(pass_me, pass_me))
    app.add_generic_role('textsc', textsc)


def skip_me(node): 
    raise nodes.SkipNode

def pass_me(node): 
    pass


#################################################################
# Setup Configurations


def setup(app):
    
    app.add_builder(BookBuilder)
    
    # Adds all custom nodes, roles, and directives ('thought', 'synopsis', ...)
    add_nodes(app)
        
    # REQUIRED. Sets the title.
    app.add_config_value('bacch_title', None, '')

    # REQUIRED. Sets the author name.
    app.add_config_value('bacch_author', None, '')

    # Changes the layout. Opens up the 'notitle' option.
    app.add_config_value('bacch_nonsubmission', False, '')

    # Removes the title page if nonsubmission = True.
    app.add_config_value('bacch_notitle', False, '') 

    # Uses chapters, changes to novel layout.
    app.add_config_value('bacch_novel', False, '')

    # Tweaks the layout. One of: anon, baen, daw, wotf.
    app.add_config_value('bacch_submission_type', None, '')

    # Changes quote behavior. One of: smart, dumb.
    app.add_config_value('bacch_quote_type', None, '')         

    # Overrides the default monospace font.
    app.add_config_value('bacch_courier', False, '')           

    # Changes papersize. One of: a4paper, letterpaper.  
    app.add_config_value('bacch_papersize', None, '')

    # Changes the scene separator from "#". 
    app.add_config_value('bacch_sceneseparator', None, '')     

    # Changes the end-of-story symbol from "# # # # #".  
    app.add_config_value('bacch_thirty', None, '')

    # Overrides the running header with arbitrary LaTeX.
    app.add_config_value('bacch_msheading', None, '')    
    
    # Sets the title in the running header, overriding the title.
    app.add_config_value('bacch_runningtitle', None, '')        
    
    # Sets your real name, if that differs from your nom de plume.
    app.add_config_value('bacch_authorname', None, '')        

    # Sets the name in the running header, overriding the author. 
    app.add_config_value('bacch_surname', None, '')

    # Provides a free-form multi-line address. Use triple quotes.           
    app.add_config_value('bacch_address', None, '')

    # Sets the wordcount manually, or if None, suppresses entirely.
    app.add_config_value('bacch_wordcount', 'default', '')     

    # Marks the document as disposable. 
    app.add_config_value('bacch_disposable', False, '')        

    # Changes to one space between sentences.
    app.add_config_value('bacch_frenchspacing', False, '')    

    # Doublespaces verse instead of single-spacing. 
    app.add_config_value('bacch_doublespace_verse', False, '')
    




