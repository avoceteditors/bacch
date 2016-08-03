##########################################################################
# Module Imports
import os, os.path
import re

##########################################################################
# Reader Class
class Reader():

    # Initialize Class
    def __init__(self, config):
        self.config = config

        # Load File List
        filelist = self.get_filelist()


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
                    "filename": i,
                    "path": path
                }

        return file_list
    


