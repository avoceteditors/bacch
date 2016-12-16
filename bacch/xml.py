# Module Imports
import lxml.etree 
import bacch

# Read File
def read_xml(path):

    bacch.log.debug("XML Reader: %s" % path)

    # Open File
    f = open(path, 'rb')
    content = f.read()
    f.close()

    # Initialize Doctree
    try:
        doctree = lxml.etree.fromstring(content)
    except:
        bacch.log.debug("XML Reader: Failed")
        doctree = None 

    return doctree

# Fetch Elements
def fetch_element(doctree, element):
    return doctree.xpath(element, namespaces = bacch.__xmlns__)

