#! /usr/bin/env python3

##################################################################
# bacch.py - Provides a series of utilities to assist writers    #
#  working in unix-like environments, such as Linux and FreeBSD. #
#  These utilities include a project builder for presentation, a #
#  compiler of project statistics and progress, and similar      #
#  development tools for technical writers and novelists.        #
#                                                                #
# Author: Kenneth P. J. Dyer                                     #
#                                                                #
# Version: 0.1                                                   #
#                                                                #
# Date: Janauary 2015                                            #
#                                                                #
##################################################################


#####################################
# Module Imports

import sys, argparse, os, os.path, configparser
import lxml, lxml.etree, lxml.ElementInclude


####################################
# Classes

class Project():

    # Parse Config File
    def parse_config(self, path):
        if path == None:
            self.title == 'Untitled Project'
            self.author == 'Unnamed Author'
            self.work == 'Undefined Project Type'
        else:
            config = configparser.ConfigParser()
            config.read_file(open(path))



    # Initialize Class
    def __init__(self, args):
        

        # Initialize Locations
        sourcelist = [ 'source/',
                       'src/' ]
        outputlist = [ 'build/',
                       'output/']
        
        xmlindex = [ 'index.xml',
                     'book.xml']
        restindex = [ 'index.rst',
                     'index.txt']
        tmp = 'tmp/'

        # Initialize Arugment Variable
        path = args.set_path
        form = args.set_format
        output = args.output
        target = args.target
        standalone = args.standalone

        # Initialize Class Variables
        self.path = ''
        self.form = 0
        self.config = ''
        self.title = ''
        self.author = ''
        self.work = ''
        self.source = ''
        self.build = ''
        self.sourcefiles = {}
        self.target = 0
        self.index = []
        home = os.path.expandvars('$HOME')

        self.tmp = ''
        self.configscan = [ home + '/.config/bacch/' ]

        

        # Define Path
        if path:
            if os.path.isdir(path):
                self.path = path
        else:
            self.path = './'
        
        # Define Source Path
        for i in sourcelist:
            source = self.path + i
            if os.path.exists(source):
                if os.path.isdir(source):
                    self.source = source
        if not self.source:
            sys.exit("Error: No source directory.")
            
        # Build sourcefile dictionary
        for i in os.listdir(self.source):
            self.sourcefiles[i] = self.source + i


        # Define Format
        if form:
            if form.lower() == 'xml':
                print("Reading project as XML.")
                self.index = xmlindex
                self.form = 1
            elif form.lower() == 'rst':
                print("Reading project as reStructuredText")
                self.index = restindex
                self.form = 2
            elif form.lower() == 'rest':
                print("Reading project as reStructuredText")
                self.index = restindex
                self.form = 2

            elif form.lower() == 'restructuredtext':
                print("Reading project as reStructuredText")
                self.index = restindex
                self.form = 2
            else:
                sys.exit("Error: Invalid read format.")

        else:
            listing = os.listdir(self.source)
            xml = rest = 0
            for key in self.sourcefiles:
                extension = str(self.sourcefiles[i])[-4:]
                if 'xml' in extension:
                    xml = xml + 1
                elif 'rst' in extension:
                    rest = rest + 1

            if xml > rest:
                print("Reading project as XML.")
                self.index = xmlindex
                self.form = 1
            elif xml < rest:
                print("Reading project as reStructuredText")
                self.index = restindex
                self.form = 2
            else:
                sys.exit("Error: Unable to determine read format.\n \t Consider using bacch with the --set_format option.\n")



        # Set Output Format
        workpath = ''
        if target:
            if target == 'html'.lower() and standalone:
                print("Defining Output as Standalone HTML.")
                self.target = 1
            elif target == 'html'.lower():
                print("Defining Output as HTML")
                workpath = 'html/'
                self.target = 2
            elif target == 'pdf'.lower() and standalone:
                print("Defining Output as Standalone PDF.")
                self.target = 3
            elif target == 'pdf'.lower():
                print("Defining Output as Chapter Formatted PDF")
                workpath = 'pdf/'
                self.target = 4
            elif target == 'docx'.lower() or target == 'doc':
                if standalone:
                    print("Defining Output as Standalone Microsoft Word Document")
                    self.target = 5
                else:
                    print("Defining Output as Chapter Formatted Microsoft Word Document")
                    workpath = 'word/'
                    self.target = 6
        else:
            print("Defining Output as HTML")
            self.target = 2



        # Define Build Path
        if output:
            if os.path.isdir(output):
                if output[-1] != '/':
                    self.output = output + '/'
                else:
                    self.output = output

                self.tmp = '/' + tmp + 'bacch/'
            else:
                self.output = 'build/' + workpath
                self.tmp = self.path + tmp 
        else:
            self.output = 'build/' + workpath
            self.tmp = self.path = tmp

        print("Build output path defined as %s." % self.output)

    ############################################
    # File Locator
    def find_file(self,target):
        for path in self.configscan:
            if os.path.exists(path + target):
                if os.path.isfile(path + target):
                    return path + target
        sys.exit("Error: Unable to locate %s file." % target)


    ############################################
    # Class Build Methods

    # XML Builder
    def build_xml(self):

        print("Building project from XML.")
        
        root = []
        standalone = [1,3,5]
        latex = [3,4,5,6]
        if self.target in standalone:
            for key in self.sourcefiles:
                if key in self.index:
                    root = [self.sourcefiles[key]]
                else:
                    root.append(self.sourcefiles[key])
        else:
            for key in self.sourcefiles:
                if 'xml' in key[-4:]:
                    root.append(self.sourcefiles[key])
                
        # Find Stylesheet
        if self.target == 1:
            xsl = self.find_file('standalone-html.xsl')
        elif self.target == 2:
            xsl = self.find_file('html.xsl')
        elif self.target == 3:
            xsl = self.find_file('standalone-pdf.xsl')
        elif self.target == 4:
            xsl = self.find_file('pdf.xsl')
        elif self.target == 5:
            xsl = self.find_file('standalone-doc.xsl')
        elif self.target == 6:
            xsl = self.find_file('doc.xsl')

        # Find Extension
        if self.target in [1,2]:
            extension = 'html'
        elif self.target in latex:
            extension = 'tex'

        self.extension = extension
        self.xsl = xsl

        output = ''
        if self.target in standalone:
            self.buildstand_xml()
        else:
            self.buildall_xml()


    def buildstand_xml(self):
        print("Running XML Standalone Builder")
    

    def buildall_xml(self):
        print("Running XML Master Builder")

        tree = lxml.etree.parse(self.source + '/book.xml')
        tree.xinclude()
        xslt = lxml.etree.parse(self.xsl)
        transform = lxml.etree.XSLT(xslt)
        output = str(transform(tree))

        if self.extension == 'html':
            outputfile = self.output + 'master.html'
            flag = ''
            if os.path.exists(outputfile):
                flag = 'w'
            else:
                flag = 'x'

            f = open(outputfile, flag)
            f.write(output)
            f.close()

            
    # reST Builder
    def build_rest(self):
        print("Building project from reStructuredText.")



    ############################################
    # Class Structural Update Methods

    # XML Struct Updater
    def struct_xml(self):
        import lxml.etree as ET
        print("Updating structure from XML.")

    # reST Struct Updater
    def struct_rest(self):
        print("Updating structure from reStructuredText.")


    ########################################
    # Class Database Update Methods

    # XML DB Updater
    def data_xml(self):
        import lxml.etree as ET
        print("Updating database from XML.")

    # reST DB Updater
    def data_rest(self):
        print("Updating database from reStructuredText.")



####################################
# Subparser Functions

# Project Builder
def builder(arguments, thisProject):
    print("Running Project Build")
    
    if thisProject.form == 1:
        thisProject.build_xml()
    elif thisProject.form == 2:
        thisProject.build_rest()
    else:
        sys.exit("Nothing to do.")



# Project Strcuture Updater
def struct(arguments, thisProject):
    print("Running Structural Updater")

    if thisProject.form == 1:
        thisProject.struct_xml()
    elif thisProject.form == 2:
        thisProject.struct_rest()
    else:
        sys.exit("Nothing to do.")


# Project Database Updater
def data_compiler(arguments, thisProject):
    print("Running Project Data Compiler")
    if thisProject.form == 1:
        thisProject.data_xml()
    elif thisProject.form == 2:
        thisProject.data_rest()
    else:
        sys.exit("Nothing to do.")



#####################################
# Main Function

def main():
    print("Initializing bacch")

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Base Arugments
    parser.add_argument('--force', action="store_true")
    parser.add_argument('-s','--standalone',action="store_true")
    parser.add_argument('--set_path')
    parser.add_argument('--set_config')
    parser.add_argument('-f','--set_format')
    parser.add_argument('-o','--output')
    parser.add_argument('-t', '--target')

    
    # Subparser for Building Projects
    build = subparsers.add_parser('build')
    build.set_defaults(func=builder)

    
    # Subparser for Updating Projects
    update_structure = subparsers.add_parser('struct')
    update_structure.set_defaults(func=struct)

    # Subparser for Data Functions
    dataread = subparsers.add_parser('data')
    dataread.set_defaults(func=data_compiler)

    # Parse Arguments and Call Relevant Functions
    args = parser.parse_args()


    # Initialize Project Class
    thisProject = Project(args)

    # Launch Argument Functions
    args.func(args, thisProject)

sys.exit(main())
