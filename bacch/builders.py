""" Provides the Bacch and Gnomon builder classes, as well as
the Base superclass to organize common methods between them. """
# Copyright (c) 2017, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the name of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from sphinx.builders import Builder
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.console import darkgreen, bold
from sphinx.util.osutil import ensuredir
from sphinx.application import TemplateBridge

from os.path import join, exists, dirname
from shutil import copyfile
from .writer import LaTeXWriter

from subprocess import run


############################################
# Base Superclass for Bacch/Gnomon Builders
class BaseBuilder(Builder):
    """ Base Class for managing the Bacch and Gnomon builders."""
    writer = None

    # Prepare Build
    def prepare_build(self, docnames):

        # Find Template
        template = None
        fname = self.name + '.tex'
        for i in self.config.templates_path:
            template_path = join(self.env.srcdir, i, fname)
            if exists(template_path):
                template = (template_path, fname, dirname(template_path))
                break

        # Prepare Writer
        self.writer = LaTeXWriter(self.config, self.name, template)

        # Prepare Output Directory
        self.outtmp = join(self.outdir, 'tmp')
        for i in [self.outdir, self.outtmp]:
            ensuredir(i)

        # Run Local Preparations
        self.local_prep(docnames)

    # Assemble Doctree
    def assemble_doctree(self, master):
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set(), master, tree, darkgreen, [master])
        tree['docname'] = master
        self.env.resolve_references(tree, master, self)

        return tree

    # Write
    def write(self, *ignored):

        # Fetch Docnames
        docnames = self.env.all_docs

        # Prepare Documents
        self.info(bold("Preparing Documents..."), nonl=True)
        self.prepare_build(docnames)
        self.info("Done")

        # Build Documents
        for master in self.masters:

            # Compile Docuument
            self.info("Compiling: %s" % master, nonl=True)
            doctree = self.assemble_doctree(master)
            self.info("Done")

            # Write Document
            self.info("Writing Document: %s" % master, nonl=True)
            self.write_doc(master, doctree)
            self.info("Done")

    # Write Document
    def write_doc(self, docname, doctree):

        # Write LaTeX File
        texpath = join(self.outtmp, docname + '.tex')
        with open(texpath, 'w') as f:
            self.writer.write(doctree, f)

        # Generate PDF 
        latex_builder = self.config.bacch_pdfbuild

        if latex_builder is not None and self.config.bacch_pdf:
            if latex_builder == 'lualatex':
                command = [latex_builder, '--output-directory=%s' % self.outtmp, texpath]

                # Build PDF
                self.pdf(command, docname, texpath)

            # Error Out if Invalid
            else:
                raise ValueError("Invalid PDF Builder: %s" % latex_builder)

    # Finish Build
    def pdf(self, command, docname, texpath):

        # Configure Paths
        tmppath = join(self.outtmp, docname + '.pdf')
        pdfpath = join(self.outdir_pdf, docname + '.pdf')

        if exists(texpath):
            run(command)

            # Run Build Again If Toc
            if getattr(self.config, '%s_tocpage' % self.name):
                for i in range (1,2):
                    run(command)

            # Copy File
            copyfile(tmppath, pdfpath)

        else:
            self.info(bold("Unable to Locate Output TeX"), nonl=False)


############################################
# Bacch Builder Class for Building Books
class BacchBuilder(BaseBuilder):
    """ Subclass for Bacch Builder, used in converting the overall
    project from a collection of reStructuredText files to a single
    LaTeX document."""

    name = 'bacch'

    # Initialize Class
    def init(self):
        self.outdir_pdf = self.outdir


    # Fetch Outdated Documents
    def get_outdated_docs(self):
        return 'all documents'

    # Run Local Preparations
    def local_prep(self, docnames):
        self.masters = self.config.bacch_masters


############################################
# Gnomon Builder Class for Building Articles
class GnomonBuilder(BaseBuilder):
    """ Subclass for Gnomon Builder, used in converting individual
    files from reStructuredText to chapter-formatted LaTeX."""

    name = 'gnomon'

    # Run Local Preparations
    def local_prep(self, docnmaes):

        # Set Temporary master
        self.masters = self.config.bacch_masters
        print("\n\nWARNING: Temporary Masters still in Use\n\n")
