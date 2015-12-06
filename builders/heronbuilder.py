#!/usr/bin/env python3.4

#########################
# Module Imports

import codecs, os.path, re, sphinx

from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.compat import Directive

from docutils import nodes, writers
from docutils.io import StringOutput

import writers.heronwriter as heronwriter
import re, subprocess, json

############################
# Bacch Project Builder
class HeronBuilder(Builder):

    name = "heron"
    format = "json"
    extension = ".json"
    writer = None

    # Initialization
    def init(self):
        pass
        
    # Outdated Docs
    def get_outdated_docs(self):
        return 'all documents'

    def prepare_writing(self, docnames):
        self.config.bacch_build_type = 'heron'
        self.writer = heronwriter.HeronWriter(self.config)


    # Get Relative URI's
    def get_relative_uri(self, docname, typ):
        return '%' + docname


    # Write Function
    def write(self, *ignored):
        docnames = self.env.all_docs

        # Prepare Documents
        self.info(bold("Preparing documents..."), nonl=True)
        self.prepare_writing(docnames)
        self.info("Done")

        # Assemble Doctree
        self.info(bold("Assembling singular document..."), nonl=True)
        doctree = self.assemble_doctree()
        self.info("Done")

        # Write Document
        self.info(bold("Writing singular document.."), nonl=True)
        self.write_doc(self.config.master_doc, doctree)

        self.outfile = os.path.join(self.outdir, 
                                    os_path(self.config.master_doc) + '.json')
   
        ensuredir(os.path.dirname(self.outfile))
        self.write_file(self.outfile, self.writer.output)
        self.info("Done")

    # Build Doctree
    def assemble_doctree(self):
        master = self.config.master_doc
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
                json.dump(content, f, indent = 4)

            finally:
                f.close()
        except(IOError, OSError) as err:
            self.warn("Error writing file %s: %s" % (outfile, err))

    def finish(self):
        pass
                

    


