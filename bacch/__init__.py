# Metadata
__version__ = '0.9'
__author__ = 'Kenneth P. J. Dyer'
__author_email__ = 'kenneth@avoceteditors.com'
__name__ = 'bacch'
__print_name__ = 'Bacch'
__slogan__ = 'The Document and Static Site Generator'
__all__ = ['html']

# Module Imports
from .core import run, exit
from .loghandler import VerboseLogHandler, QuietLogHandler
from .reader import Reader
from .filehandlers import xmlHandler, fetch_element
from .dataentry import DataEntry
from .processing import *
from .preprocessor import Preprocessor

# XML Namespaces
__xmlns__ = {
    "bacch": "http://avoceteditors.com/2016/bacch",
    "book": "http://docbook.org/ns/docbook",
    "xi": "http://www.w3.org/2001/XInclude"
}
rev = {}
for key in __xmlns__:
    value = __xmlns__[key]
    rev[value] = key
__rxmlns__ = rev
