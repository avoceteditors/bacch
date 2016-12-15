# Metadata
__version__ = '0.9'
__author__ = 'Kenneth P. J. Dyer'
__author_email__ = 'kenneth@avoceteditors.com'
__name__ = 'Bacch'
__slogan__ = 'The Document and Static Site Generator'

# Module Imports
from .core import run, exit
from .loghandler import VerboseLogHandler, QuietLogHandler
from .datahandler import DataHandler
from .picklehandler import load_data, save_data
