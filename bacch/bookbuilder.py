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
from os.path import join
from sphinx.util.osutil import ensuredir
import subprocess
from shutil import copyfile

from .bookwriter import BookWriter

class BookBuilder(Builder):
    """ Subclass used in generating LaTeX documents
    formatted for book publication. """
    name = 'bacch'


    # Prepare Writing
    def prepare_document(self, docnames):

        # Configure Writer
        self.docwriter = BookWriter(self, self.config)
        self.build = 'bacch'

        # Prepare Output Directories
        self.output_path = join(self.outdir, 'tmp')
        for i in [self.outdir, self.output_path]:
            ensuredir(i)

        self._docnames = docnames


    # Collect Outdated Documents
    def get_outdated_docs(self):
        return 'all documents'

    # Assemble Doctree
    def assemble_doctree(self, master):
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set(), master, tree, darkgreen, [master])
        tree['docname'] = master
        self.env.resolve_references(tree, master, self)
        return tree

    # Write Method
    def write(self, *ignored):

        # Fetch Document Names
        docnames = self.env.all_docs

        # Prepare Documents
        self.info(bold("Preparing Documents..."), nonl=True)
        self.prepare_document(docnames)
        self.info("Done")

        # Initialize Variables
        masters = self.config.bacch_masters
        

        # Compile and Write Documents
        for master in masters:

            # Compile Document
            self.info("Compiling: %s" % master, nonl=True)
            doctree = self.assemble_doctree(master)
            self.info("Done")

            # Write Document
            self.info("Writing Document: %s" % master, nonl=True)
            self.write_doc(master, doctree)
            self.info("Done")

            
    # Write Document
    def write_doc(self, docname, doctree):

        self.info("Writing LaTeX: %s" % docname, nonl=True)

        texpath = join(self.output_path, docname + ".tex")
        # Write LaTeX File
        with open(texpath, 'w') as f:
            self.docwriter.write(doctree, f)

        # Generate PDF
        latex = self.config.bacch_pdfbuild
        if latex is not None:

            # LuaLaTeX
            if latex == 'lualatex':
                command = [latex, '--output-directory=%s' % self.output_path, texpath]
                options = self.config.bacch_pdfbuild_options
                if options is not None:
                    command = command + options

                self.pdf_build(command, docname)
            else:
                raise ValueError("Invalid PDF Builder: %s" % latex)


    # Generate PDF
    def pdf_build(self, command, docname):
        tmppath = join(self.output_path, docname + ".pdf")
        pdfpath = join(self.outdir, docname + ".pdf")

        if getattr(self.config, '%s_toc' % self.build):
            for i in range(1,4):
                subprocess.run(command)
        else:
            subprocess.run(command)

        # Move File
        copyfile(tmppath, pdfpath)







