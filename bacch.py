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

import sys, argparse, os

####################################
# Classes




####################################
# Subparser Functions

# Project Builder
def builder(arguments):
    print("Running Project Build")

# Project Updater
def updater(arguments):
    print("Running Project Update")

# Project Data
def data_compiler(arguments):
    print("Running Project Data Compiler")



#####################################
# Main Function

def main():
    print("Initializing bacch")

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Subparser for Building Projects
    build = subparsers.add_parser('build')
    build.set_defaults(func=builder)

    # Subparser for Updating Projects
    update = subparsers.add_parser('update')
    update.set_defaults(func=updater)

    # Subparser for Data Functions
    dataread = subparsers.add_parser('data')
    dataread.set_defaults(func=data_compiler)

    # Parse Arguments and Call Relevant Functions
    args = parser.parse_args()
    args.func(args)



sys.exit(main())