# Copyright (c) 2015, Kenneth P. J. Dyer
# All rights reserved.
#
# Redistribution and use in source and binary forms, 
# with or without modification, are permitted provided 
# that the following conditions are met:
#
# * Redistributions of source code must retain the 
#   above copyright notice, this list of conditions 
#   and the following disclaimer.
#
# * Redistributions in binary form must reproduce the 
#   above copyright notice, this list of conditions 
#   and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of bacch nor the names of its 
#   contributors may be used to endorse or promote 
#   products derived from this software without 
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS 
# AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED 
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING 
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN 
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



# Writer Module
#
# This is the control module for output.  
# The Controller gives it the pseudo-XML
# from the Reader module.  It  determines 
# the desired output, (PDF or ODF), going
# off the configs or args.  Then it calls 
# the relevant translator moduule to generate
# the results.
#
# Dev the translator files later.  Focus on 
# LaTeX/PDF first, with ODF introduced 
# secondary, (given that it'll prove more 
# difficult to write).
#
# In some cases the Writer module needs to hit 
# hte database module for updated 
# information, such as in the case where it needs 
# to produce word counts or graphs
# defining the state of the project.
#
# Writer Module outputs data to file.  It also 
# calls postprocessing, such as converting
# LaTeX into a PDF, or XML into ODT.

# Module Imports
import re
import site
import lxml.etree as ET
import os
import os.path

from bacch import lib
from bacch import pdfwriter

# Writer Class
class Writer():

    def __init__(self, args, data):
        if args.verbose:
            lib.report("Initializing writer...", 0)


        db = "http://docbook.org/ns/docbook"
        build = args.build
        if build == 'pdf':
            self.writer = pdfwriter.PDFWriter(args)
        else:
            raise SyntaxError(
                    "Error: Bacch does not support"
                    " %s output." % build)
        args.tmpdir = os.path.join(
                args.output, 'tmp')
        paths = [args.output, args.tmpdir]
        self.ensuredirs(paths, args)
        self.parse_data(args, data)
        self.writer.get_text()

    def parse_data(self, args, data):
        self.writer.visit_set(data)
        self.parse(args, data)
        self.writer.depart_set(data)



    def parse(self, args, root):


        nodes = root.childNodes
        for node in nodes:

            name = node.nodeName
            if name[0] == '#':
                name = name[1:].upper()
            elif ':' in name:
                name = re.sub(':', '__', name)
           

            if name is not None:
                check = eval('self.writer.visit_%s(node)' % name)
                if check or check is None and node.hasChildNodes():
                    self.parse(args, node)
                eval('self.writer.depart_%s(node)' % name)

    def evaluate(self, args, node, name):
        check = eval('self.writer.visit_%s(node)' % name)
        if check and node.hasChildNodes():
            self.parse(args, node)
        eval('self.writer.depart_%s(node)' % name)

    def ensuredirs(self, paths, args):
        if args.verbose:
            lib.report("Checking Directory Paths...", 1)


        for path in paths:
            if not os.path.exists(path):
                if args.verbose:
                    lib.report(
                        "Path %s doesn't exist, creating..." % path, 2)
                os.mkdir(path)
            else:
                if args.verbose:
                    lib.report(
                        "Path %s exists." % path, 2)



