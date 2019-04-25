"""
    Bacch LaTeX builder

    Code baed on sphinx.builders.latex, which has been 
    modified to support more general book publications.
"""

# Module Imports

# Docutils
from docutils import nodes
from docutils.frontend import OptionParser
from docutils.io import FileOutput

# Sphinx
from sphinx import addnodes, highlighting
from sphinx.builders import Builder
from sphinx.util import texescape, logging
from sphinx.environment import NoUri
from sphinx.util.osutil import SEP
from sphinx.builders.latex import LaTeXBuilder

import os.path

from .write import BacchLaTeXWriter


# Init Logger
logger = logging.getLogger(__name__)

class BacchBuilder(LaTeXBuilder):

    name = 'bacch'
    format = 'latex'
    epilog = "Bacch LaTeX Build is available in %(outdir)s"

    def init(self):
        self.docnames = []
        self.document_data = []
        self.usepackages = []
        self.build_map = False 
        texescape.init()

    def write_stylesheet(self):
        highlighter = highlighting.PygmentsBridge(
                'latex', self.config.pygments_style, self.config.trim_doctest_flags)
        stylesheet = os.path.join(self.outdir, 'sphinxhighlight.sty')
        writes = [ '\\NeedsTeXFormat{LaTeX2e}[1995/12/01]\n',
                '\\ProvidesPackage{sphinxhighlight}',
                '[2016/05/29 ',
                'stylesheet for highlighting with pygments]\n',
                highlighter.get_stylesheet()]

        with open(stylesheet, 'w') as f:
            for w in writes:
                f.write(w)

    def build_all(self):
        self.build_map = True
        self.build()

    def init_document_data(self):

        if self.build_map:
            preliminary_document_data = [list(x) for x in self.config.bacch_documents]
        else:
            if self.config.bacch_index is not None:
                preliminary_document_data = [self.config.bacch_documents[self.config.bacch_index]]
            else:
                preliminary_document_data = [self.config.bacch_documents[0]]

        # Check Valid
        if not preliminary_document_data:
            logger.warning('no "latex_documents" config value found; no documents '
                           'will be written')
            return
        # assign subdirs to titles
        self.titles = []  # type: List[Tuple[unicode, unicode]]
        for entry in preliminary_document_data:
            docname = entry[0]
            if docname not in self.env.all_docs:
                logger.warning('"latex_documents" config value references unknown '
                               'document %s', docname)
                continue
            self.document_data.append(entry)  # type: ignore
            if docname.endswith(SEP + 'index'):
                docname = docname[:-5]
            self.titles.append((docname, entry[2]))

    def fetch_template(self, name):

        # Find Template File
        template_dir = self.config.templates_path
        data = None
        for i in template_dir:
            template_path = os.path.join(self.env.srcdir, i)
            filename = name + '.tex'
            path = os.path.join(template_path, filename)
            if os.path.exists(path):
                data = (template_path, filename) 
                break
        return data 


    def write(self, *ignored):

        docwriter = BacchLaTeXWriter(self)
        docsettings = OptionParser(
                defaults=self.env.settings,
                components=(docwriter,),
                read_config_files=True).get_default_values()

        self.init_document_data()
        self.write_stylesheet()

        for entry in self.document_data:
            docname, targetname, title, author, docclass = entry[:5]
            toctree_only = False

            # Find Template Path 
            length = len(entry)
            if length > 5:
                template_name = entry[4]
            else:
                template_name = 'bacch'
            template_path = self.fetch_template(template_name)

            if length > 6:
                toctree_only = entry[5]
            destination = FileOutput(
                    destination_path=os.path.join(self.outdir, targetname),
                    encoding='utf-8')

            logger.info("processing %s...", targetname, nonl=1)
            toctrees = self.env.get_doctree(docname).traverse(addnodes.toctree)

            tocdepth = None
            if toctrees:
                if toctrees[0].get('maxdepth') > 0:
                    tocdepth = toctrees[0].get('maxdepth')
                else:
                    tocdepth = None

            doctree = self.assemble_doctree(
                    docname, toctree_only,
                    appendices=((docclass != 'howto') and self.config.latex_appendices or []))
            doctree['tocdepth'] = tocdepth
            self.apply_transforms(doctree)
            self.post_process_images(doctree)

            logger.info('writing...', nonl=1)
            doctree.settings = docsettings
            doctree.settings.author = author
            doctree.settings.title = title
            doctree.settings.contentsname = self.get_contentsname(docname)
            doctree.settings.docname = docname
            doctree.settings.docclass = docclass
            docwriter.template_path = template_path
            docwriter.title = title
            docwriter.write(doctree, destination)
            logger.info('done')

