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
import sys, argparse, os, os.path, configparser, shutil
import lxml, lxml.etree, lxml.ElementInclude
import sphinx

class Project():

    def __init__(self, args):

        # Build Masthead
        self.program = "bacch"
        self.version = "0.3"
        self.masthead = "%s version %s\n" % (self.program, self.version)

        print(self.masthead)

        # Load Arguments into Class
        self.args = args




        
# Launch Program
if __name__ == '__main__':

    # Parse Arguments
    parser = argparse.ArgumentParser()

    arguments = parser.parse_args()
    thisProject = Project(arguments)
