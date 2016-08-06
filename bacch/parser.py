##########################################################################
# Module Imports
import subprocess

from bacch import core as bacch_core

##########################################################################
# Parser Class
class Parser():

    def __init__(self, config, base_data):

        # Initialize Variables
        self.config = config
        self.name = base_data['name']
        self.filename = base_data['filename']
        self.path = base_data['path']


        # Read File
        f = open(self.path, 'r')
        content = f.read()
        f.close()


