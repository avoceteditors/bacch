#!/usr/bin/env python3.4

#########################
# Module Imports

import codecs, os.path, re, sphinx

from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path, SEP
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.compat import Directive

from docutils import nodes, writers
from docutils.io import StringOutput

import writers.bacchwriter as bacchwriter
import utils.platform as platform

import subprocess

#########################
# Bacch Project Builder
class GnomonBuilder(Builder):

    name = "gnomon"
    format = "latex"
    extension = ".tex"
    writer = None
    system = platform.BacchSystem()
    texfiles = []
    
    # Initialization
    def init(self):
        pass
    
    # Outdated Docs
    def get_outdated_docs(self):
        return self.env.all_docs

    # Prepare Writing
    def prepare_writing(self, docnames):
        self.writer = bacchwriter.BacchWriter(self.config,
                                              "gnomon")

    # Get Relative URI's
    def get_relative_uri(self, docname, typ):
        return '%' + docname

    def get_target_uri(self, docname, typ=None):
        if docname == 'index':
            return ''

        if docname.endswith(SEP + 'index'):
            return docname[:-5]

        return docname + SEP

    def get_outfilename(self, pagename):
        if pagename == 'index' or pagename.endswith(
                SEP + 'index'):

            outfilename = os.path.join(
                self.outdir,
                os_path(pagename) + self.extension)
        else:
            outfilename = os.path.join(
                self.outdir,
                pagename + self.extension)
        return outfilename
    
    # Write Function
    def write(self, *ignored):
        docnames = self.env.all_docs

        # Prepare Documents
        self.info(bold("Preparing documents..."), nonl=True)
        self.prepare_writing(docnames)
        self.info("Done")

        # Write Document
        self.info(bold("Writing documents.."), nonl=True)

        for i in docnames:
            doctree = self.assemble_doctree(i)
            self.write_doc(i, doctree)
            outfile = self.get_outfilename(i)
            ensuredir(os.path.dirname(outfile))
            self.texfiles.append(outfile)
            self.write_file(outfile, self.writer.output)
            self.info("Done %s" % i)

    # Build Doctree
    def assemble_doctree(self, master):
        #master = self.config.master_doc
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self,set(),master,tree,darkgreen)
        tree['docname'] = master

        return tree

    # Write Document
    def write_doc(self, docname, doctree):
        destination = StringOutput(encoding = 'utf-8')
        output = self.writer.write(doctree, destination)

    # Write Files
    def write_file(self, outfile, content):
        try:
            f = codecs.open(outfile, 'w', 'utf-8')
            try:
                f.write(content)
            finally:
                f.close()
        except(IOError, OSError) as err:
            self.warn("Error writing file %s: %s" % (outfile, err))

    # Final Process
    def finish(self):
        for i in self.texfiles:
            latex = self.system.latex(self.outdir, i)
            print(latex)
