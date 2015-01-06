#! /usr/bin/env python3

#############################################################
# install.py - Installation script for bacch.py.  Copies    #
#  all relevant files to their appropriate locations.  You  #
#  should run this after repo updates.  Note: It requires   #
#  root permissions.                                        #
#                                                           #
# Author: Kenneth P. J. Dyer                                #
#                                                           #
#############################################################


##############################
# Module Imports
import platform, sys, os, os.path

##############################
# File Functions

# Create Necessary Directories if None Exist
def path_checker(paths):
    for path in paths:
        print("[Check] Status of %s..." % path)
        if os.path.isfile(path):
            print("[Error] %s directory is a file.\n")
            sys.exit(2)
        elif os.path.isdir(path):
            print("[Load] %s\n" % path)
        elif not os.path.exists(path):
            print("[Create] %s\n" % path)
            os.mkdir(path)
            

###############################
# Installation Functions

# Linux Installer
def linux_install():
    print("Beginning Linux Installation...\n")

    # Configure Paths
    directories = ["/usr/lib/python3/dist-packages/bacch/",
                   "/etc/bacch/"]
    path_checker(directories)


    return 0

###############################
# Main Function
def main():
    system = platform.system()
    print("Starting bacch Installer\n")

    # Check User Platform
    if system == "Linux":
        sys.exit(linux_install())
    else:
        print("Error: bacch does not support %s systems." % system)
        sys.exit(1)



    

main()



