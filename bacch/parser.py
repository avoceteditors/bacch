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


        # Fetch Document Stats
        bacch_core.log(self.config.verbose, 'info', "--Logging stats")
        args = ['words', 'lines', 'chars']
        setattr(self, 'document_stats', ParserObject)
        for arg in args:
            opt = '--' + arg
            data = subprocess.check_output(['wc', opt, self.path]).decode().split(' ')[0]
            setattr(self.document_stats, arg, int(data))

            



##########################################################################
# Parser Object
class ParserObject():
    pass
