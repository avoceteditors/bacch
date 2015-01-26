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

import sys, argparse, os, os.path

####################################
# Classes

###################################
# General Functions


# Remove Temporary Files
def clean_listing(path):
    newlist = []
    listing = os.listdir(path)

    for i in listing:
        filename = path + i
        if os.path.isfile(filename):
            if i[-1] != "~" and i[-1] != "#":
                newlist.append(filename)
    return newlist


# Differentiate between ReST/XML
def find_source():
    listing = os.listdir('.')
    source = ""
    if 'source' in listing:
        source = "./source/"
    elif 'src' in listing:
        source = "./src/"
    else:
        print("Error: This is not a project directory")
        sys.exit(1)

    listing = clean_listing(source)
    return listing

# Find Most Recent Change
def find_most_recent(filelist):
    print("Determine Most Recent Source File")
    mtime = 0

    for i in filelist:
        stats = os.stat(i)
        modtime = stats.st_mtime
        if modtime > mtime:
            mtime = modtime
    return mtime

def check_status(source, checkfile):
    print("Determine Project Status")
    project_modtime = find_most_recent(source)
    test = False
    check = checkfile

    if os.path.exists(struct_file):
        stats = os.stat(struct_file)
        struct_modtime = stats.st_mtime
        if project_modtime > struct_modtime:
            test = True
    else:
        test = True

    return test

# Determine If XML or reStructuredText Project
def classify_project(source):
    xml = rst = 0
    for i in source:
        extension = i[-4:]
    
        if extension == ".xml":
            xml = xml + 1
        elif extension == ".rst":
            rst = rst + 1

    if xml < rst:
        print("Project classified as reStructuredText")
        return 1
    elif xml > rst:
        print("Project classified as XML")
        return 2
    else:
        print("No classification found")
        return 0

###################################
# General Reader Functions

# Read reStructuredText
def read_rest(sourcelist, action):
    print("Reading in reStructuredText")

    # Find Config File
    config = ''
    if './source/conf.py' in sourcelist:
        config = './source/conf.py'
    elif '.config' in os.listdir('.'):
        # Call Configreader
        pass
    else:
        print("Unable to find configuration file.")
        sys.exit(1)
    

        
# Read XML
def read_xml(sourcelist, action):
    print("Reading in XML")



####################################
# Subparser Functions

# Project Builder
def builder(arguments, sources, project_type):
    print("Running Project Build")


    # Determine if source files are more 
    #   recent than struct.json
    status = check_status(source_list, os.listdir('build'))
    
    if status or arguments.force:
        print("Starting Project build")

        # Launch Readers
        if project_type == 1:
            read_rest(sources, 1)
        elif project_type == 0:
            read_xml(sources, 1)

    else:
        print("Project up to date.")
    
    
# Project Strcuture Updater
def struct(arguments, sources, project_type):
    print("Running Project Update")


    # Determine if source files are more 
    #   recent than struct.json
    status = check_status(source_list, ["./.struct.json"])

    if status or arguments.force:
        print("Updating Project struct")
        
        # Launch Readers
        if project_type == 1:
            read_rest(sources, 0)
        elif project_type == 2:
            read_xml(sources, 0)

    else:
        print("Project struct up to date.")



# Project Data
def data_compiler(arguments):
    print("Running Project Data Compiler")



#####################################
# Main Function

def main():
    print("Initializing bacch")

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Base Arugments
    parser.add_argument('-f', '--force', action="store_true")
    parser.add_argument('-s','--standalone',action="store_true")
    
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


    # Read Source Directory and log files
    print("Check project directory...\n")
    source_list = find_source()

    # Classify Project
    project_type = classify_project(source_list)


    # Launch Argument Functions
    args.func(args, source_list, project_type)



sys.exit(main())
