##########################################################################
# Module Imports
import os, os.path
import re

from bacch import core as bacch_core
from bacch import parser as bacch_parser

##########################################################################
# Reader Class
class Reader():

    # Initialize Class
    def __init__(self, config):
        self.config = config

        # Load File List
        filelist = self.get_filelist()

        # Parse Source
        for key in filelist:
            bacch_core.log(self.config.verbose, 'debug',
                    '-Parsing: %s' % filelist[key]['filename'])

            # Parse File
            data = bacch_parser.Parser(config, filelist[key])

            # Log Files
            filelist[key]["data"] = data
        self.data = filelist

    # Determine File List
    def get_filelist(self):
        """ Return List of Files in Source Directory

        This method reads all files in the source directory, then sorts
        out any that do not have the proper extension, as defined by the
        system_extension parameter.  By default, it looks for %.rst files.
        """

        base_list = os.listdir(self.config.system_source)
        file_list = {}
        ext = self.config.system_extension
        
        for i in base_list:
            if re.match('.*.%s$' % ext, i):
                (name, ext) = os.path.splitext(i)
                path = os.path.abspath(
                        os.path.join(self.config.system_source, i))
                file_list[name] = {
                    "name": name,
                    "filename": i,
                    "path": path
                }

        return file_list
    

    # Return Filelist
    def fetch_data(self):
        return self.data
