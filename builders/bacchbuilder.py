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

import writers.basewriter as basewriter
import re, subprocess, shutil

############################
# Bacch Project Builder
class BacchBuilder(Builder):

    name = "bacch"
    format = "latex"
    extension = ".tex"
    writer = None

    # Initialization
    def init(self):
        pass
        
        
    # Outdated Docs
    def get_outdated_docs(self):
        return 'all documents'

    def prepare_writing(self, docnames):
        self.config.bacch_build_type = 'bacch'
        self.writer = basewriter.BaseWriter(self.config)


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
        
        extension = '.tex'
        writer_type = self.config.bacch_output_format.lower()
        if writer_type == 'pdf':
            interext = '.tex'
            finext = '.pdf'
        elif writer_type == 'odf':
            raise ValueError("Bacch current does not support ODF output.")
 
        
        self.interfile = os.path.join(self.outdir,
                                    os_path(self.config.master_doc) + interext)
        self.tmpfile = os.path.join(self.outdir,
                                    os_path(self.config.master_doc) + finext)
        title = re.sub(' ','', self.config.bacch_title)
        self.outfile = title + finext

        
        ensuredir(os.path.dirname(self.interfile))
        self.write_file(self.interfile, self.outfile, self.tmpfile,
                        writer_type, self.writer.output)
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
    def write_file(self, interfile, outfile, tmpfile, typ, content):
        if typ == 'pdf':
            command = ['pdflatex', '--output-directory', self.outdir,
                       interfile]
        try:
            f = codecs.open(interfile, 'w', 'utf-8')
            try:
                f.write(content)
                try:
                    subprocess.call(command)
                    subprocess.call(command)
                    subprocess.call(command)
                    subprocess.call(command)
                except subprocess.CalledProcessError as e:
                    self.warn(e.output.decode())
                shutil.copyfile(tmpfile, outfile)
            finally:
                f.close()
        except(IOError, OSError) as err:
            self.warn("Error writing file %s: %s" % (outfile, err))

    def finish(self):
        pass
                

    


