# Copyright (c) 2017, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the name of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import datetime
import logging

from sys import exit as sys_exit
from os import chdir, getcwd
from os.path import exists, isdir

from .project import Project

# Global Variables
logger = None
timer_start = None
version = "0.11"


########################################
# Exit Process
def exit(exit_code=0):
    """ This function controls the exit process"""

    # Set Exit Time
    timer_end = datetime.datetime.now()

    # Calculate Run Time
    timer_diff = timer_end - timer_start
    sec = round(timer_diff.total_seconds(), 2)
    msg = "\nOperation completed in %s seconds" % sec
    print(msg)

    # Exit
    sys_exit(exit_code)


########################################
# Masthead and Logger Config Process
def run_masthead(verbose):
    """ This method runs the masthead and configures
    the logging module"""

    # Fetch Logger
    global logger

    ###########################
    # Configure Masthead and Log Handlers
    handlers = {}
    if verbose:

        # Configure Masthead
        content = [
            "Bacch: The Document Generator",
            "Kenneth P. J. Dyer <kenneth@avoceteditors.com>",
            "Avocet Editorial Consulting",
            "Version %s" % version
        ]
        masthead = "\n  ".join(content)

        # Configure Logging Handlers
        formatter_stream = logging.Formatter(
                "%(levelname)s ( %(filename)s:%(funcName)s() ): %(message)s")

        # Logging Level
        level = logging.DEBUG

    else:

        # Configure Masthead
        masthead = "Bacch: The Document Generator - Version %s" % version

        # Configure Logging Handlers
        formatter_stream = logging.Formatter(
                "%(levelname)s: %(message)s")

        # Logging Level
        level = logging.WARNING

    ##########################
    # Masthead
    print(masthead)

    ###########################
    # Initialize Logger
    logger = logging.getLogger()


    # Stream Handler
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(formatter_stream)
    logger.addHandler(handler_stream)

    # Set Level
    logger.setLevel(level)


########################################
# Main Process
def run(args):
    """ This function controls the main process"""

    # Init Timer
    global timer_start
    timer_start = datetime.datetime.now()

    # Masthead
    run_masthead(args.verbose)

    # Start Bacch
    logger.info("Starting Bacch")

    # Set Working Directory
    logger.debug("Configuring Working Directory")
    
    if exists(args.working_dir):
        if isdir(args.working_dir):
            chdir(args.working_dir)

    # Initialize Project
    project = Project()

    # Exit
    exit(0)
