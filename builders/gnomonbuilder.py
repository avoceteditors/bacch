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

import writers.basewriter as basewriter
import subprocess, shutil

#########################
# Gnomon Project Builder
class GnomonBuilder(Builder):

    name = "gnomon"
    format = "latex"
    extension = ".tex"
    writer = None
    textfiles = []


    # Initialization
    def init(self):
        pass
        
    # Outdated Docs
    def get_outdated_docs(self):
        return self.env.all_docs

    def prepare_writing(self, docnames):
        self.config.bacch_build_type = 'gnomon'
        self.writer = basewriter.BaseWriter(self.config)

    # Get Relative URI's
    def get_relative_uri(self, docname, typ):
        return '%' + docname

    def get_target_uri(self, docname, typ=None):
        if docname == 'index':
            return ''

        if docname.endswith(SEP + 'index'):
            return ''

        return docname + SEP

    def get_filename(self, directory, pagename, extension):
        if pagename == 'index' or pagename.endswith(
                SEP + 'index'):

            outfilename = os.path.join(
                directory,
                os_path(pagename) + extension)
        else:
            outfilename = os.path.join(
                directory,
                pagename + extension)
        return outfilename

    
    def write(self, *ignored):
        docnames = self.env.all_docs

        # Prepare Documents
        self.info(bold("Preparing documents..."), nonl=True)
        self.prepare_writing(docnames)
        self.info("Done")

        # Write Document
        self.info(bold("Writing documents.."), nonl=True)
        writer_type = self.config.gnomon_output_type
        interext = '.tex'
        outext = '.pdf'
        if writer_type == 'pdf':
            interext = '.tex'
            outext = '.pdf'
        elif writer_type == 'odf':
            pass
        
        tmpdir = os.path.join(self.outdir, 'tmp')            
        for i in docnames:
            if i != 'index':
                doctree = self.assemble_doctree(i)
                self.write_doc(i, doctree)

                interfile = self.get_filename(tmpdir, i, interext)
                tmpfile = self.get_filename(tmpdir, i, outext)
                outfile = self.get_filename(self.outdir, i, outext)
                ensuredir(os.path.dirname(interfile))
                self.write_file(interfile, tmpfile, outfile, tmpdir,
                                writer_type, self.writer.output)
                self.info("Done %s" % i)
            else:
                self.info("Skipping %s" % i)

    def assemble_doctree(self, master):
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self,set(),master,tree,darkgreen)
        tree['docname'] = master

        return tree

    # Write Document
    def write_doc(self, docname, doctree):
        destination = StringOutput(encoding = 'utf-8')
        output = self.writer.write(doctree, destination)


    # Write Files
    def write_file(self, interfile, tmpfile,
                   outfile, tmpdir, typ, content):

        if typ == 'pdf':
            command = ['pdflatex', '--output-directory', tmpdir,
                       interfile]
        try:
            f = codecs.open(interfile, 'w', 'utf-8')
            try:
                f.write(content)
                try:
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
