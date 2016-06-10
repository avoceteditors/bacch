# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of bacch nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


################# Notes ############################
# Placeholder for new main process for Bacch.
#
# This module receives arguments from commnand-line script,
# it then feeds in and out to manage the various processes
# in the application.

# Module Imports
import sys
import site
import os, os.path
import configparser
import pickle

from bacch import reader
from bacch import lib
from bacch import writer
# Controller Class
class Bacch():
    """ Main Controller for Bacch

    Bacch: Document Generator

    Primary controller class for Bacch.  Receives 
    arguments from the command-line, then uses 
    them to initialize the main processes.
    """



    # Initialize Class
    def __init__(self, args):
        version = '0.7'
        version_line = 'Version %s' % version

        # Print Masthead
        masthead = ["Bacch: The Document Generator"]
        if args.verbose:
            extra = [
              'Kenneth P. J. Dyer',
              'Avocet Editorial Consultants',
              'kenneth@avoceteditors.com',
              version_line
            ]
            print('\n  '.join(masthead + extra) + '\n')
        elif args.version:
            print(' - '.join(masthead + [version_line]) + '\n')
            sys.exit(0)

        xml = reader.Reader(args)
        xml_parser = writer.Writer(args, xml.fetch())


