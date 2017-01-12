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

        # Read Source
        self.data = {}
        self.update()

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
                self.resources[name] = self.build_dict(
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
                self.builds[name] = self.build_dict(attr, bdict)
            except:
                pass

        # Reader Configuration
        base_readers = bacch.fetch_element(master,
            '%s/bacch:readers/bacch:reader' % configxpath)
        rdict = {'extension': 'xml'}
        self.readers = {}
        for i in base_readers:
            attr = i.attrib
            try:
                name = attr['name']
                self.readers[name] = self.build_dict(attr, rdict)
            except:
                pass
                
    # Build Configuration Dictionary
    def build_dict(self, attr, targets):
        """ This method generates a dict object from
        configuration values retrieved from master.xml.
        """
        
        ret_dict = {}
        
        # Loop Target Dict 
        for key in targets:

            # Set Configuration Value
            try:
                ret_dict[key] = attr[key]

            # Set Default Value
            except:
                ret_dict[key] = targets[key] 

        return ret_dict
             

    # Update Reads
    def update(self):
        """ This method controls the file read process, building
        a list of relevant files and starting the read."""

        # Set Base Directory
        base_path = os.path.abspath(os.getcwd())
       
        # Generate Extension Listings 
        exts = ['.xml', '.md']

        # Process Resources
        for key in self.resources:
            config = self.resources[key]
            if config['type'] in ['source', 'blocks']:
                sourcepath = os.path.join(base_path, config['path'])
                base = os.listdir(sourcepath)

                # Initialize Key in self.data
                if key not in self.data:
                    self.data[key] = {}
                
                # Iterate over Files in Directory
                for i in base:
                    self.process_file(key, i, sourcepath)

        # Set Section Data
        self.set_sects()

    # Process File Instance
    def process_file(self, key, filename, sourcepath):
        """ This method provides processing for individual files
        in a given resource.  For each file, it tests whether the
        file is one that it knows how to handle then checks if it
        has an old read available.  If it doesn't have an old read
        or if it does and finds that read out of date, it generates
        a new instances of the bacch.DataEntry() class.  """

        split = os.path.splitext(filename)
        name = split[0]
        ext = split[1]

        # Match Files to Parse
        if ext in ['.xml']:

            # Set Path
            path = os.path.join(sourcepath, filename)

            # Try Reading from Data
            try:
                entry = self.data[key][name]

                if bacch.__args__.sync:
                    if entry.check_mtime():
                        self.init_dataentry(key, name, path)

            # Create New Entry
            except:
                self.init_dataentry(key, name, path)

    # Init Data Entry
    def init_dataentry(self, key, name, path):
        """ This helper method parses the given path into
        an lxml doctree, it then initializes a bacch.DataEntry()
        class instance, which it adds to self.data."""  

        data = self.read(path)
        self.data[key][name] = bacch.DataEntry(name, path, data)

    # Retrieve Data
    def fetch(self):
        """ This method retrieves read data from the class."""
        return self.data

    # Set Sectional Data
    def set_sects(self):
        """ This method sets sectional data for the class by
        retrieving each from each file read DataEntry() class.
        """
        self.sect_data = {}

        for resource in self.data:
            self.sect_data[resource] = {}

            for i in self.data[resource]:
                element = self.data[resource][i]

                sects = element.fetch_sects()
                for sect in sects:
                    entry = sects[sect]
                    entry['href'] = i
                    self.sect_data[resource][sect] = entry
    

    # Retrieve Sectional Data
    def fetch_sects(self):
        """ This method retrieves sectional data for the given
        files.  This is passed in the form of a dict that contains
        each resource and every section idref in the resource."""
        return self.sect_data 
