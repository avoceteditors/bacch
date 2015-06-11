#! /usr/bin/evn python3

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

import tex

import bacchwriter

#######################################
# Project Builder
class BacchFullBuilder(Builder):
    name = "fullbacch"
    format = "latex"
    extension = ".tex"
    writer=None

    def init(self):
        pass

    def get_outdated_docs(self):
        return 'all documents'

    def prepare_writing(self,docnames):
        self.writer = bacchwriter.BacchWriter(self.config, self.name)

    def get_relative_uri(self,from_,to,typ=None):
        return self.get_target_uri(to,typ)

    def get_target_uri(self,docname,typ):
        return '%' + docname

    def write(self, *ignored):
        docnames = self.env.all_docs

        # Prepare Documnets
        self.info(bold("Preparing documents..."),nonl=True)
        self.prepare_writing(docnames)
        self.info("Done")

        # Assemble Doctree
        self.info(bold("Assembling singular document..."),nonl=True)
        doctree = self.assemble_doctree()
        self.info("Done")

        # Write Document
        self.info(bold("Writing singular document..."),nonl=True)
        self.write_doc(self.config.master_doc,doctree)
        self.outfile = os.path.join( self.outdir,
                                     os_path( self.config.master_doc) +
                                     self.extension)
        self.docfile = os.path.join( 
            self.outdir,
            os_path( 
                self.config.bacch_title.lower().replace(' ','') +
                '.pdf'))

        ensuredir(os.path.dirname(self.outfile))
        self.write_file(self.outfile,self.writer.output)
        self.info("Done")
        

    # Build the Doctree
    def assemble_doctree(self):
        master = self.config.master_doc
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self,set(),master,tree,darkgreen)
        tree['docname'] = master

        return tree

    # Write Document
    def write_doc(self,docname,doctree):
        destination = StringOutput(encoding = 'utf-8')
        output = self.writer.write(doctree,destination)

    # Write Files
    def write_file(self,outfile,content):
        try:
            f = codecs.open(outfile,'w','utf-8')
            try:
                f.write(content)
            finally:
                f.close()
        except (IOError, OSError) as err:
            self.warn("Error writing file %s: %s" % (outfile,err))

    def finish(self):
        pass
                        

        
########################################
# Chapter Builder
class BacchChapBuilder(Builder):
    name = 'chapbacch'
