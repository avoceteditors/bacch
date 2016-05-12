# Copyright (c) 2015-2016, Kenneth P. J. Dyer
# All rights reserved.
# 
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

# Module Imports
import os
import os.path

from bacch import config as bacch_config
from bacch import builder as bacch_builder


# Initialize Main Process Class
class Bacch():
    """ Bacch: The reStructuredText Document Generator

    This is the primary class for the Bacch process.  Functions
    called from the bacch CLI initialize and operate through this
    class.
    """

    # Initialize Class
    def __init__(self, args):
        self.args = args

        self.paths = {}
        self.create_dirs = []
        self.create_files = []

        # Check Directory Paths
        base_dirpaths = ['source', 'output', 'configdir']
        for name in base_dirpaths:
            arg = getattr(args, name)
            path = os.path.abspath(arg)
            self.paths[name] = path

            if os.path.exists(path):
                if not os.path.isdir(path):
                    raise ValueError('Error: %s is not a directory.' % arg)
            else:
                self.create_dirs.append(path)




    ############# Initialization Process ##################
    def init_project(self):
        
        # Create Directories 
        if self.args.verbose:
            print("Checking Directory Structure...")
        length = len(self.create_dirs)
        if length > 0:
            self.create_directories()
        else:
            if self.args.verbose:
                msg = [' - Source Directory: \t%s' % self.paths['source'],
                       ' - Output Directory: \t%s' % self.paths['output'],
                       ' - Config Directory: \t%s' % self.paths['configdir']]
                print('\n'.join(msg))



        # Check Files
        self.paths['config'] = config =  self.check_file(self.args.config, 'config')
        self.paths['database'] = database = self.check_file(self.args.database, 'db', True)
        self.paths['log'] = log = self.check_file(self.args.log, 'log', True)

        if self.args.verbose:
            print("Checking Configuration File Structure...")
            msg = [' - Config File: \t%s' % config,
                   ' - Database: \t\t%s' % database,
                   ' - Log File: \t\t%s' % log
                   ]
            print('\n'.join(msg))


    # Create Directories
    def create_directories(self):
    
        dirs = self.create_dirs
        if self.args.verbose:
            print("  Creating directories...")
            for i in dirs:
                print('  - %s' % i)

        for i in dirs:
            os.mkdir(i)
        print("Done.")

    # Define File Paths
    def check_file(self, name, typ, config = False):
        
        file_path = os.path.abspath(name)
        dir_path = os.path.abspath(
                os.path.join(self.args.configdir, name))

        if os.path.exists(file_path):
            return file_path
        elif os.path.exists(dir_path):
            return dir_path
        else:
            if typ == "config":
                self.init_config(file_path)
        
            return dir_path
    

    def init_config(self, path):
        print("Method to Initialize Configuration File",
                "(NOTE: Feature not yet implemented)")


    ############## Configuration #######################
    def get_config(self):

        config = self.parse_config()
        builders = config["System"]["builders"]
        build = self.args.builder

        if build not in builders:
            build = builders[0]

        try:
            check = config["Build"][build]
        except:
            raise ValueError("Error: Invalid Builder: %s" % build)

        return [config, build]

    # Parse the Config
    def parse_configs(self):

        config_sys_path = os.path.abspath(
                os.path.join(site.USER_SITE,
                    'bacch', 'config', 'main.conf'))
        config_user_path = self.paths['config']

        if self.args.verbose:
            print("Initializing Configuration File...")
            msg = [' - Opening User Configuration File: \t%s' % config_user_path,
                    ' - Opening System Configuration File: \t%s' % config_sys_path]
            print('\n'.join(msg))

        config_user = configparser.ConfigParser()
        config_user.read(config_user_path)

        config_sys = configparser.ConfigParser()
        config_sys.read(config_sys_path)

        # Parse Config Files
        config = {
            "System": {},
            "Metadata": {},
            "Build": {}
        }

        
        default_configs = [config_sys, config_user]
        default_units = ["System", "Metadata"]

        for unit in default_units:
            for key in config_sys[unit]:
                for conf in default_configs:
                    try:
                        config[unit][key] = conf[unit][key]
                    except: 
                        pass

        builders = config['System']['builders'].split(',')
        config['System']['builders'] = builders

        for build in builders:
            config['Build'][build] = {}
            for key in config_sys["Default"]:
                try:
                    config['Build'][build][key] = config_user[build][key]
                except:
                    config['Build'][build][key] = config_sys['Default'][key]

        return config

    ############### Build Process #######################
    def build_project(self):
        
        # Initialize Project
        self.init_project()

        config = self.get_config()


        builder = bacch_builder.Builder(self.args, config[0], config[1])        



