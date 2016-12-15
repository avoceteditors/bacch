# Module Imports
import os
import bacch

# Data Handler
class DataHandler():

    def __init__(self, master = 'master.xml'):

        # Initialize Namespaces
        self.ns = {
            "bacch": "http://avoceteditors/2016/bacch",
            "book": "http://docbook.org/ns/docbook",
            "xi": "http://www.w3.org/2001/XInclude"
        }

    def sync(self):

        if bacch.sync:
            return True
        else:
            return False

    def update(self):
        pass        
