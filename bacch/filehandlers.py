""" This module provides core handlers for reading files
from XML, Markdown and reStructuredText.  Whatever the
format, it converts it to DocBook XML then passes it into
the lxml module to generate a doctree."""

# Module Imports
import lxml.etree
import bacch

# Fetch Element
def fetch_element(doctree, element_path):
    return doctree.xpath(element_path,
        namespaces = bacch.__xmlns__)

# Fetch Doctree
def fetch_doctree(content):
    """ This function receive a string containing what it
    assumes is DocBook XML.  It then parses it into an
    lxml.etree._Element and returns the doctree."""

    # Init Doctree
    try:
        doctree = lxml.etree.fromstring(content)
    except:
        bacch.__log__.debug("XML Reader: Failed %s" % path)
        doctree = None
    return doctree 

# Read XML
def xmlHandler(path):
    """ This function provides a general handlers for
    parsing XML files to lxml objects."""

    # Open File
    f = open(path, 'rb')
    content = f.read()
    f.close()

    return fetch_doctree(content)

# Read Markdown
def mdHandler(path):
    """ This function provides a general handler for
    converting Markdown files to DocBook XML, then
    parsing into lxml objects."""

    bacch.__log__.warning("Markdown parsing not supported for %s" % path)
    raise ValueError("Bacch cannot yet parse Markdown")


# Read reStructuredText 
def rstHandler(path):
    """ This function provides a general handler for
    converting reStructuredText files to DocBook XML,
    then parsing into lxml objects."""

    bacch.__log__.warning("RST parsing not supported for %s" % path)
    raise ValueError("Bacch cannot yet parse RST")

