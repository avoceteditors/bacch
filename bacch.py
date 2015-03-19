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
# Version: 0.2                                                   #
#                                                                #
# Date: March 2015                                               #
#                                                                #
##################################################################


###################################
# Module Imports
import sys, argparse, os, os.path, configparser, shutil
import lxml, lxml.etree, lxml.ElementInclude
import sphinx


###################################
# Main Class

class Project():

    # Initialize Arguments and Class
    def __init__(self):
        self.masthead = "bacch version 0.2" 
        print(self.masthead)

        # Init Project Variables
        self.source = ''
        self.path = ''
        self.build = ''
        self.config = ''
        self.confpy = ''
        self.project_type = 0
        self.config_index = ''
        
        # Init Metadata
        self.title = 'Untitled'
        self.subtitle = ''
        self.author = 'Unknown Author'
        
        
    def init_args(self,args):

        self.verbose = args.verbose
        self.force = args.force
        self.buildall = args.buildall
        self.standalone = args.standalone

        # Define Path
        if self.verbose:
            print("Defining Program Variables:")
            print("\tValidating path...")
        path = args.set_path
        if path:
            if os.path.isdir(path):
                self.path = path
        else:
            self.path = './'
        if self.verbose:
            print("\tSetting path to %s\n" % self.path)
 
        # Set Source
        self.sourcepath = self.path_checker(
            0, args.set_source,['src/','source/'], "source")
        
        # Set Build
        self.buildpath = self.path_checker(
            0, args.set_build, ['build/'], 'build')

        # Find Default Files
        self.config = self.path_checker(
            1, args.set_config, ['.config'], 'config')
        self.config_reader()

        # Determine Project Type:
        self.source_classifier(args.read_format)

        self.reader = args.read_format
        self.target = args.target_format

        
        # Launch Processor
        if args.task == 'build': 
            self.builder()
        elif args.task == 'struct':
            self.struct()
        elif args.task == 'data':
            self.data()
        else:
            print("Error: Invalid Task")
            sys.exit(1)


    # Path Checker
    def path_checker(self, check, checkpath, defaults, name):
        
        if self.verbose:
            print("\tValidating %s path..." % name)
        result = ''
        if checkpath:
            if os.path.isdir(checkpath) or os.path.isfile(checkpath):
                result = checkpath
        else:
            for i in defaults:
                check = self.path + i
                if os.path.exists(check):
                    result = check
                    break
            if result == '':
                result = self.path + defaults[0]
                if check == 0:
                    os.mkdir(result)
                elif check == 1:
                    with open(path, defaults[0]):
                        os.utime(path, None)

            if self.verbose:
                print('\tPath to %s not found.' % name )
                print('\tCreating %s' % result)
                print('\tSetting %s to %s\n' % (name, result))
            return result
                    
        if self.verbose:
            print("\tSetting %s to %s\n" % (name, result))
            return result
                
    # File Checker
    def file_checker(self, path):
        paths = [path, self.sourcepath + '/' + path]
        result = ''
        for i in paths:
            if os.path.exists(i):
                if os.path.isfile(i):
                    result = i
                    break
        
        return result
                    
    # Config Reader
    def config_reader(self):
        if self.verbose:
            print('Reading Configuration File at %s' % self.config)
        config = configparser.ConfigParser()
        config.read_file(open(self.config))

        # Set Metadata
        self.title = self.set_config(config, 'Metadata', 'title')
        self.subtitle = self.set_config(config, 'Metadata', 'subtitle')
        self.author_full = self.set_config(config,'Metadata','author_full')
        self.author_sur = self.set_config(config,'Metadata','author_sur')

        # Set Project Data
        self.source_type = self.set_config(config, 'Project','source_type')
        self.project_type = self.set_config(config,'Project','project_type')
        self.confpy = self.set_config(config,'Project', 'confpy')
        self.config_index = self.set_config(config,'Project','index')
        
    def set_config(self, parser, unit, value):
        try:
            return parser[unit][value]
        except:
            return "Unknown"

    # Project Classification
    def source_classifier(self,argument):
        if self.verbose:
            print("Source file classification:")


        if argument != None:
            if self.verbose:
                print("\tSource files classified as %s" % argument)
            self.source_type = argument.lowercase()
        elif self.source_type == "Unknown":
            if self.verbose:
                print("\tSource files unlcassified by %s" % self.config)
                print("\tDetermining source file classification...")
            listing = os.listdir(self.sourcepath)
            xml = rst = 0    
            for i in listing:
                if i[-3:] == 'xml':
                    xml = xml + 1
                elif i[-3:] == 'rst':
                    rst = rst + 1
                    
            # Check Results
            if rst > xml:
                self.source_type = 'rst'
            elif rst < xml:
                self.source_type = 'xml'
            else:
                print("Error: Unable to determine source file classification.")
                sys.exit(1)
                
        # Source Classification
        if self.verbose:
            print("\tSource files classified as %s" % self.source_type)
            

        # Find Stylesheet and conf.py
        if self.verbose:
            print("Locating extended configuration file")

        if self.source_type == 'rst':
            
            paths = [ os.environ['HOME'] + '/repo/bacch/config/conf.py',
                      os.environ['HOME'] + '/.config/bacch/conf.py',
                      '/usr/share/bacch/conf.py']

            check = self.sourcepath + '/conf.py'
            if not os.path.exists(check):
                for i in paths:
                    if os.path.exists(i):
                        shutil.copyfile(i, check)
                        break
            
                      
            if self.verbose:
                print("\tExtended configuration file identified as %s\n" % self.confpy)

        # Find Start Position
        if self.verbose:
            print("Start Position:")

        if self.config_index != 'Unknown':
            self.index = self.file_checker(self.config_index)

        elif self.source_type == 'rst':
            listing = os.listdir(self.sourcepath)
            index = ['index.rst', 'index.txt', 'book.rst']
            for i in index:
                if i in listing:
                    self.index = self.file_checker(i)
                    break
        elif self.source_type == 'xml':
            listing = os.listdir(self.sourcepath)
            index = ['index.xml', 'book.xml']
            for i in index:
                if i in listing:
                    self.index = self.file_checker(i)
                    break        
        if self.verbose:
            print("\tSetting start position at %s\n" % self.index)

    #########################################        
    # Builder Method
    def builder(self):
        print("Initializing Builder")

        # Determine Output Format
        if self.verbose:
            print("Determining build output format:")
        output_format = 'html'
        if self.target != None:
            output_format = self.target.lower()
            listing = ['html', 'pdf', 'docx']
            if target not in listing:
                print("Error: Unidentified target output format.")
                sys.exit(1)
        if self.verbose:
            print("\tSetting target output to %s\n" % output_format)
        self.target = output_format
            
        # reStructuredText Builder
        if self.source_type == 'rst':
            self.rst_builder()
            
        # XML Builder
        elif self.source_type == 'xml':
            self.xml_builder()
            
    #############################################    
    # Struct Method
    def struct(self):
        print("Initializing Structural Reader")

    #############################################
    # Data Method
    def data(self):
        print("Initializing Data Reader")



    #############################################
    # Builder Methods
        
    # reStructuredText Builder
    def rst_builder(self):
        print("Initializing Sphinx")
        options = ['','-b',self.target]
        if self.buildall:
            options.append('-a')
        arguments = options + [self.sourcepath, self.buildpath]
           
        sphinx.main(arguments)

    # XML Builder
    def xml_builder(self):
        print("Initializing XML Builder")
        
##################################
# Initialize Main Process
if __name__ == '__main__':
    # Initialize Class
    thisProject = Project()
    run = 0

    # Initialize Argument Parser
    parser = argparse.ArgumentParser()
    
    # Base Arguments
    parser.add_argument('task',
                        choices = ['build', 'struct', 'data'] )
    parser.add_argument('--force', action="store_true")
    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument('--set_path')
    parser.add_argument('--set_config')
    parser.add_argument('--set_source')
    parser.add_argument('--set_build')
    parser.add_argument('-a', '--buildall')
    parser.add_argument('-s','--standalone')
    parser.add_argument('-r','--read_format')
    parser.add_argument('-t','--target_format')

    # Parse Arguments
    arguments = parser.parse_args()
    sys.exit(thisProject.init_args(arguments))


