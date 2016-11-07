# Module Imports
import bacch.blocks

import xml.etree.ElementTree as etree

def block(xml, level = 0, data = None):

    blocks = []
    for element in xml:

        tag = element.tag
        block = None

        if tag == 'p':
            block = bacch.blocks.Paragraph(element)

        else:
            print("Error: Unidentified Element: %s" % tag)


        # Append Block
        if block is not None:
            blocks.append(block)

    return data



