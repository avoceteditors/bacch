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

# Module Imports
import os, os.path
from bacch import lib
#import lxml.etree as ET
import re
import xml.dom.minidom as minidom

# Reader Class
class Reader():

    # Initialize Class
    def __init__(self, args):

        args.level = 0
        if args.verbose:
            lib.report("Initializing Reader...", args.level)

        # Define Source
        args.level += 1
        if args.verbose:
            lib.report("Defining source file.", args.level)
        source = os.path.abspath(
                self.set_source(args.source))
         
        if args.verbose:
            lib.report("Setting source file to:", 
                    args.level)
            lib.report(source, args.level + 1)


        args.sourcedir = os.path.dirname(source)
        self.data = self.read_file(args, source)

    def fetch(self):
        return self.data


    # Define Source File 
    def set_source(self, source):
        """ Determine Source File for Build

        Method receives the source argument
        set from command-line, checks whether
        source is a file or directory.  If file,
        it returns arg.  If directory, it checks
        that master.xml exists in that directory,
        then returns that.
        """
      
        if self.check_file(source):
            return source
        else:
            source = os.path.join(source, 'master.xml')
            if self.check_file(source):
               return source 
            else:
                raise ValueError(
                        "Error: No Source File")
            
            
    def check_file(self, filename):
        """ Checks that Filename exists and is File

        Utility method.  Receives a filename as an
        argument, checks that file exists and that
        it is a file.  If both true, returns True,
        otherwise it returns False.
        """
        if os.path.exists(filename):
            if os.path.isfile(filename):
                return True
        return False

    def read_file(self, args, path):
        if args.verbose:
            lib.report("Reading File.")
 
        document = minidom.parse(path)
        root = document.documentElement
        data = self.parse(args, document, root)
        #data = ET.parse(path)
        #root = data.getroot()
        #for element in root.iter():
        #    tag = str(element.tag)
        #    if re.match('^{.*}include',tag):
        #        href = os.path.join(
        #                self.sourcedir,
        #                element.attrib['href'])
        #        if args.verbose:
        #            level = args.level + 1
        #            lib.report(
        #                    "Found XInclude: %s"
        #                    % href, level)
        #            self.read_file(args, href)
       
        return data

    def parse(self, args, document, root):

        nodes = root.getElementsByTagName('*')
        for node in nodes:
            tag = node.tagName
            if tag == "xi:include":
                filename = node.getAttribute('href')
                href = os.path.join(args.sourcedir, filename)
                if args.verbose:
                    lib.report("Found XInclude: %s" % filename)
                data = self.read_file(args, href)

                node.setAttribute('bacch:filename', href)
                mtime = os.path.getmtime(href)
                node.setAttribute('bacch:mtime', mtime)
                node.appendChild(data)

        return root

