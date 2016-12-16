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
from .xml import read_xml, fetch_element
from .dataentry import DataEntry
from .builders import PageBuilder, BookBuilder

# XML Namespaces
__xmlns__ = {
    "bacch": "http://avoceteditors.com/2016/bacch",
    "book": "http://docbook.org/ns/docbook",
    "xi": "http://www.w3.org/2001/XInclude"
}
