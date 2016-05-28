# Copyright (c) 2015, Kenneth P. J. Dyer
# All rights reserved.

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


# Reader Module
#
# Receives a file list from the controller, then calls on classes to
# parse the individual rst files into a pseudo-XML format, which represents
# the structural makeup of the project.  Returns the XML to the controller
# for use in further operations.
#
# It may be useful to cache the XML to help in speeding up overall processes.
# For instance, Sphinx has an issue when building full documents in that it has
# to run end to end from scratch.  With cached XML ready, it check the mtimes
# on the files against the cache, then only update the relevant XML at this stage.

# Module Imports
import os, os.path

class Reader():
    """ Reader Controller

    Secondary Controller Class for Bacch.  Called by the controller
    class and passed command-line arguments and the base configuration.

    Reader determines what files it needs to read then parses the
    out of date files into XML, pickling the updates.  It then passes
    XML objects back to the controller.
    """

    def __init__(self, args, config):
        self.args = args
        self.config = config

        if self.args.verbose:
            print("Initializing Reader...")

        source = self.config.sourcedir
        pickle = os.path.join('.bacch', 'pickle', 'files')

        master = self.config.builders[self.config.build]['master_doc']
        ext = self.config.builders[self.config.build]['suffix']
        if ext[0] == '.':
            ext = ext[1:]

        directory = ReadDirectory(args, config, source, pickle, ext)
        self.manifest = directory.manifest


# Directory Handler
class ReadDirectory():
    """ Directory Handler for Reader Class

    Receives arguments, configuration, source and pickle directories,
    as well as the target suffix from Reader().  Class then reads the
    relevant directories to build a file manifest.  Manifest is a dict
    where each name contains a dict providing the paths to the source
    and pickle files as well as a boolean value defining whether the
    Reader() should update or create the pickle.
    """

    def __init__(self, args, config, source, pickle, ext):
        self.args = args
        self.config = config
        self.manifest = {}
        if self.args.verbose:
            print('   Loading directory information...')

        # Build Source List
        self.find_source(source, pickle, ext)
        self.check_mtimes()


    def find_source(self, source, pickle, ext):

        os.chdir(source)
        base_list = os.listdir('.')
        for entry in base_list:
            name_split = entry.split('.')
            if name_split[-1] == ext:
                name = name_split[0]
                src_path = os.path.abspath(entry)
                pick_path = os.path.abspath(
                    os.path.join(pickle, name + '.pickle')
                )

                self.manifest[name] = {
                    "source_path": src_path,
                    "pickle_path": pick_path,
                    "update": True
                }

    def check_mtimes(self):

        for entry in self.manifest:
            src_path = self.manifest[entry]['source_path']
            pick_path = self.manifest[entry]['pickle_path']

            # Check Source mtime
            src_mtime = os.path.getmtime(src_path)

            # Check Pickle
            if os.path.exists(pick_path):
                pick_mtime = os.path.getmtime(pickpath)

                if src_mtime < pick_mtime or self.args.update:
                    update = True
                else:
                    update = False
                    if self.args.verbose:
                        print('Logging %s to load from pickle' % entry)
            else:
                update = True

            self.manifest[entry]['update'] = update
