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
# Version: 0.3                                                   #
#                                                                #
# Date: April 2015                                               #
#                                                                #
##################################################################


###################################
# Module Imports
import sys, argparse, os, os.path, configparser, shutil, subprocess
import lxml, lxml.etree, lxml.ElementInclude
import sphinx

class Project():

    
    def __init__(self, args):

        # Build Masthead
        self.program = "bacch"
        self.version = "0.3"
        self.masthead = "%s version %s" % (self.program, self.version)

        self.ignorelist_start = ['#']
        self.ignorelist_end = ['#', '~']

        # Initialize Variables
        self.path = ''
        self.sourcedir = ''
        self.outputdir = ''
        self.meta = {}
        
        # Load Arguments into Class
        self.args = args

        # Initialize Working Directory
        self.init_dir()

        # Initialize Builders
        self.init_build()
        
    # Initialize Working Directory
    def init_dir(self):
        if self.args.verbose:
            print(self.masthead)

        # Initialize Path
        path = self.args.path
        try:
            if os.path.isdir(path):
                self.path = os.path.realpath(path)
        except:
            self.path = os.path.realpath('.')
        
        # Add a Slash to Path If None
        self.path = self.fix_dirpath(self.path)

        # Verbose Notification
        if self.args.verbose:
            print("\t Defining working directoy as %s." % self.path)

        # Find Configuration File
        configfile = self.args.config
        default = 'project.conf'
        if configfile != None:
            if os.path.exists(configfile) and os.path.isfile(configfile):
                configfile = default
        else:
            configfile = default
                
        # Load Configuration File
        self.config = configparser.ConfigParser()
        self.config.read(configfile)

        # Verbose Notification
        if self.args.verbose:
            print("\t Defining configuration file as %s." % configfile)
        
        # Define Project Directories
        self.sourcedir = self.parse_config("sourcedir",
                                           self.args.source, 'source', 0)
                                           
        self.outputdir = self.parse_config("outputdir",
                                           self.args.output, "tmp", 0)


        self.progdir = self.parse_config("progdir",
                                           self.args.progdir,
                                           "/usr/share/bacch/config/",0)
        self.progdir = self.fix_dirpath(os.path.realpath(self.progdir))

        # Define Reader and Writer Formats
        self.reader = self.parse_config("read_format",
                                        self.args.read_format,"check",2)
        if self.reader == 'rest':
            self.reader = 'rst'
        elif self.reader == 'docbook':
            self.reader = 'xml'
        elif self.reader == "check":
            self.reader = self.determine_reader()

        self.writer = self.parse_config("write_format",
                                        self.args.write_format, "book",2)

        # Define Metadata Variables
        self.load_metadata(0,"bacch_title", "title", "Untitled")
        self.load_metadata(0,"bacch_subtitle","subtitle")
        self.load_metadata(0,"bacch_running_title","running_title", 
                           self.meta['bacch_title'])
        self.load_metadata(0,"bacch_secondline_title","secondline_title")

        self.load_metadata(0,"bacch_author", "author", "Unknown Author")
        self.load_metadata(0,"bacch_surname", "surname", 
                           self.meta["bacch_author"])

        # Define Typesetting Variables Here


    def parse_config(self, var, arg, default, typ):
        """
        bacch method - reads command line arguments,
        project configuration file and defaults to
        determine which variable is valid and takes
        precedent.  If none are valid, exits with error.

        typ argument takes int value to determine how
        the method reads the variable.

        0 - method parses variable as directory.
        1 - method parses variable as file.
        2 - method returns highest precedent value.

        """

        try:
            configvar = self.config["Project"][var]
        except:
            configvar = None

        precedent = [default, configvar, arg]
        order = None
        for i in precedent:
            if i != None:
                check = self.check_config(i,typ)
                if check != None:
                    order = check

        if order != None:
            if self.args.verbose:
                if order != default:
                    print("\t Redefining %s variable as %s." % (order, default))
                else:
                    print("\t Defining %s variable." % order)

            return order
        else:
            sys.exit("Error at line 121 on %s, fix." % default)


    # Check Configs
    def check_config(self, check, typ):
        if typ == 2:
            return check
        else:
            if os.path.exists(check):
                if typ == 0:
                    if os.path.isdir(check):
                        return self.fix_dirpath(check)
                if typ == 1:
                    if os.path.isfile(check):
                        return check
        return None

    def fix_dirpath(self,path):
        if path[-1:] == "/":
            return path 
        else:
            return path + '/'

    def determine_reader(self):
        sourcefiles = self.clear_ignores(os.listdir(self.sourcedir))
        rst = xml = 0
        for i in sourcefiles:
            ext = i[-3:]
            if ext == 'rst':
                rst = rst + 1
            elif ext == 'xml':
                xml = xml + 1

        if rst > xml:
            return 'rst'
        elif rst < xml:
            return 'xml'


    def clear_ignores(self,sourcelist):
        returnlist = []
        for i in sourcelist:
            if i[-1:] not in self.ignorelist_end:
                if i[0] not in self.ignorelist_start:
                    returnlist.append(i)
        return returnlist

    # Define Metadata Variables
    def load_metadata(self, typ, name, var, default = None):
        if typ == 0:
            unit = "Metadata"
        elif typ == 1:
            unit = "Typesetting"
        else:
            sys.exit("Invalid config, line 213")

        try:
            variable = self.config[unit][var]
        except:
            variable = default
        
        if variable != None:
            self.meta[name] = variable


    # Initialize Builders
    def init_build(self):
        if self.args.verbose:
            print("Initializing %s Builder..." % self.reader)

        if self.reader == "rst":
            self.builder_rst()
        elif self.reader == "xml":
            self.builder_xml()

            
    # Launch reST Builder
    def builder_rst(self):
        
        # Fix Confpy
        self.fix_confpy()

        # Set Metadata Variables
        metadata = ['']
        for key in self.meta:
            metadata = metadata + ['-D', '%s=%s' % (key, self.meta[key])]

        # Configure Write Format
        metadata = metadata + ['-D', 'bacch_build_type=%s' % self.writer]
            
        parameters = ['-b', self.program, self.sourcedir, self.outputdir]

        arguments = metadata + parameters
        print(arguments)
        # Run Sphinx
        sphinx.main(arguments)
    
    def fix_confpy(self):

        # Check for conf.py
        localconf = self.sourcedir + 'conf.py'
        repoconf = self.progdir + 'conf.py'

        if not os.path.exists(repoconf):
            sys.exit("Error: No repo conf.py.")
        elif not os.path.exists(localconf):
            if self.args.verbose:
                print("\tCreating symlink from %s to %s." %
                      (repoconf, localconf))
            os.symlink(repoconf,localconf)
        else:
            reallocal = os.path.realpath(localconf)
            realrepo = os.path.realpath(repoconf)

            if reallocal != realrepo:
                if self.args.verbose:
                    print("\t Found existing conf.py in %s. "
                          "Moving conf.py to .conf.py.old." % self.sourcedir)
                os.rename(localconf, self.sourcedir + 'old-conf.py')
                os.symlink(repoconf,localconf)


    # Launch XML Builder
    def builder_xml(self):
        pass
        
        
# Launch Program
if __name__ == '__main__':

    # Parse Arguments
    parser = argparse.ArgumentParser()

    # Define Base Arguments
    parser.add_argument('-v', '--verbose', action='store_true')

    # Define Configuration Arugments
    parser.add_argument('-p', '--path')
    parser.add_argument('-c', '--config')
    parser.add_argument('-s','--source')
    parser.add_argument('-o','--output')
    parser.add_argument('--progdir')

    # Defines Read and Write Formats
    parser.add_argument('-f','--read_format',
                        choices=['rst','rest','xml','docbook'])
    parser.add_argument('-t','--write_format',
                        choices=['book','manuscript'])
    
    arguments = parser.parse_args()
    thisProject = Project(arguments)
