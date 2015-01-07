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

def check_status(source):
    print("Determine Project Status")
    project_modtime = find_most_recent(source)
    test = False
    struct_file = "./.struct.json"

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
def read_rest(sourcelist):
    print("Reading in reStructuredText")
    struct = ""

    for i in sourcelist:
        if i[-4:] == ".rst":
            print("Now reading: %s" % i)

            # fileread_rest, reads four lines together
            # to determine if it's looking at a heading.
            # ditto for spotting toctree.
    

    print(struct)

    # Write the struct to File
    struct_file = open("./.struct.json", "w")
    struct_file.write(struct)
    struct_file.close()


# Read XML
def read_xml(sourcelist):
    print("Reading in XML")



####################################
# Subparser Functions

# Project Builder
def builder(arguments):
    print("Running Project Build")

# Project Strcuture Updater
def struct(arguments):
    print("Running Project Update")

    # Read Source Directory and log files
    print("Check project directory...\n")
    source_list = find_source()

    # Classify Project
    project_type = classify_project(source_list)

    # Determine if source files are more 
    #   recent than struct.json
    status = check_status(source_list)

    if status or arguments.force:
        print("Updating Project struct")
        
        # Launch Readers
        if project_type == 1:
            read_rest(source_list)
        elif project_type == 2:
            read_xml(source_list)


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
    args.func(args)



sys.exit(main())
