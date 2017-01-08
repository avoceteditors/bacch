""" Module provides a control class for reading the given
projcet and handling updates where relevant."""

# Module Imports
import os
import re
import bacch

##########################################
# Reader Class
class Reader():
    """ Project-level control class for managing file-level
    reads and providing methods for the core module."""

    # Initialize Class
    def __init__(self):

        # Init Variables
        self.project = {}
        
        bacch.__log__.info("Reading master.xml")
        master = self.read(bacch.__args__.master, True)

        # Configure Bacch
        self.parse_master(master)
        try:
            self.parse_master(master)
        except:
            bacch.__log__.critical("Error Parsing master.xml")
            bacch.exit(1)



    # Read File
    def read(self, path, getMaster = False):
        """ Method reads file data, determining the type
        of file that it needs to read, (XML, Markdown or
        reStructuredText, then calls the appropriate
        handler and returns the lxml data object.""" 

        # Separate Filename from Extension
        filename, extension = os.path.splitext(path)
        
        handler = getattr(bacch, '%sHandler' % extension[1:])
        data = handler(path)

        # Return Data 
        return data

    # Check MTime on Master
    def master_updated(self):
        return False


    # Parse Master for Configuration Data
    def parse_master(self, master):
        
        bacch.__log__.info("Configuring Application...")
        configxpath = '/bacch:project/bacch:config'        

        # Resource Configuration
        base_resources = bacch.fetch_element(master,
            '%s/bacch:resources/bacch:resource' % configxpath) 
 
        rdict = {
            'path': os.path.abspath('.'),
            'type': 'source',
            'default_lang': 'en'}       

        self.resources = {}
        for i in base_resources:
            attr = i.attrib
            try:
                name = attr['name']
                self.resource[name] = self.build_dict(
                    attr, rdict)
            except:
                pass

        # Build Configuration
        base_builds = bacch.fetch_element(master,
            '%s/bacch:builds/bacch:build' % configxpath)
        bdict = {
            'path': os.path.abspath(
                os.path.join('.', 'output')),
            'element': '*',
            'format': 'html'
            }
        self.builds = {}
        for i in base_builds:
            attr = i.attrib
            try:
                name = attr['name']
                self.builds[name] = self.build_dict(
                    attr, bdict)
            except:
                pass
                
    # Build Configuration Dictionary
    def build_dict(self, attr, targets):
        """ This method generates a dict object from
        configuration values retrieved from master.xml.
        """
        
        ret_dict = {}
        
        # Loop Target Dict 
        for key,value in targets:

            # Set Configuration Value
            try:
                ret_dict[key] = attr[key]

            # Set Default Value
            except:
                ret_dict[key] = value
        return ret_dict
             


