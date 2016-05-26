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

# Controller Class
class Bacch():
    """ Main Controller for Bacch

    Bacch: Document Generator

    Primary controller class for Bacch.  Receives arguments from
    the command-line, then uses them to initialize the main processes.
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


        ############### Configuration ########################
        # Set Paths
        config_sys_path = os.path.abspath(
                os.path.join(site.USER_SITE,
                    'bacch', 'config', 'main.conf'))
        config_user_path = os.path.abspath(args.config)
        config_pickle = os.path.abspath(
                os.path.join('.bacch', 'pickle', 'config.pickle')
        )
        self.mkdir_tree(['.bacch', 'pickle'])


        msg = ["Configuring Bacch..."]        
        if args.verbose:
            extra = ['Defining System Configuration:', '   ' + config_sys_path,
                   'Defining User Configuration:', '   ' + config_user_path,
                   'Defining Pickled Configuration: ', '   ' + config_pickle]
            msg = msg + extra

        if args.quiet:
            print('\n   '.join(msg))


        check = self.check_mtime([config_user_path, config_sys_path], config_pickle)


        # Load Configuration
        if check or not args.update:
            try:
                f = open(config_pickle, 'br')
                config = pickle.load(f)
                f.close()
                if args.verbose: 
                    print("   Loading Configuration Pickle")
            except:
                if args.verbose:
                    print("   Failed to Load Configuration Pickle")
                config = Config(args, config_user_path, config_sys_path)

        else:
            config = Config(args, config_user_path, config_sys_path)

        # Pickle Config
        f = open(config_pickle, 'bw')
        pickle.dump(config, f)
        f.close()


        data = reader.Reader(args, config)



    # Check Directory
    def mkdir_tree(self, paths):
        path = os.path.abspath('.')
        for i in paths:
            path = os.path.join(path, i)
            if not os.path.exists(path):
                os.mkdir(path)

    # Check Mod Time
    def check_mtime(self, source, target):
        stime = 0
        for i in source:
            try:
                source = os.path.getmtime(i)
                if stime > source:
                    stime = source
            except:
                pass

        try:
            ttime = os.path.getmtime(target)
        except:
            return False

        if stime > ttime:
            return True
        elif stime < ttime:
            return False
        else:
            raise ValueError(   "Pickler Error: Unable to check "
                                "modtime on source or pickle.")






# Configuration Class
class Config():

    def __init__(self, args, user, system):
        self.args = args


        # Load Configuration Files
        if args.quiet:
            print("   Loading System Configuration")
        self.config_sys = configparser.ConfigParser()
        self.config_sys.read(system)

        if args.quiet:
            print("   Loading User Configuration")
        self.config_user = configparser.ConfigParser()
        self.config_user.read(user)

        # Define Directories
        if args.quiet:
            print("   Defining Directories")

        self.sourcedir = self.setdir(args.source, 'System',
                'source', 'source')
        self.outputdir = self.setdir(args.output, 'System',
                'output', 'build')
        self.tmpdir = os.path.join('.bacch', 'tmp')
        paths = [self.outputdir, self.tmpdir]
        self.make_dir(paths)

        self.set_builds()
        if args.verbose:
            print("   Defining Build Configurations")

        self.set_metadata()
        if args.verbose:
            print("   Defining Metadata")
            print("   Configuration Ready")

        


    def setdir(self, arg, unit, variable, default):
       
        check = self.set_precedent(unit, variable)
        if arg != default:
            check = arg

        return check

    def make_dir(self, paths):
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

    def set_precedent(self, unit, variable):
        try:
            check = self.config_user[unit][variable]
        except:
            check = self.config_sys[unit][variable]

        return check


    def set_metadata(self):
        self.metadata = {}
        for var in self.config_sys['Metadata']:
            self.metadata[var] = self.set_precedent('Metadata', var)

    def set_builds(self):

        self.builders = {}

        # Check Builders
        try:
            builds = self.config_user["System"]["builders"]
        except:
            raise ValueError("Error: No builders defined in bacch.conf")

        builds = builds.split()
        for build in builds:
            self.builders[build] = {}
            for var in self.config_sys["Default"]:
                try:
                    check = self.config_user[build][var]
                except:
                    check = self.config_sys['Default'][var]
                self.builders[build][var] = check






