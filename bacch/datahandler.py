# Module Imports
import os
import re
import bacch

# Data Handler
class DataHandler():

    def __init__(self):

        ######################
        # Initialize Variables
        self.project = {}

        # Set Master Filename
        self.master = self.read(bacch.args.master, None, False)
        
        # Resources
        bacch.log.info('Project Read: Initializing...')
        config = '/bacch:project/bacch:config'
        base_resources = bacch.fetch_element(self.master, 
            '%s/bacch:resources/bacch:resource' % config)
        self.resources = {
            'source': None,
            'image': None,
            'blocks': None
        }
        for element in base_resources:
            attr = element.attrib
            self.resources[attr['type']] = attr['path']
       
        # Read Files
        self.project = {} 
        self.read_files()
        bacch.log.info('Project Read: Done')
        
    def read_files(self):
        sourcepath = self.resources['source']
        ext = '\.%s$' % bacch.args.extension
        base = os.listdir(sourcepath)

        for i in base:
            path = os.path.join(sourcepath, i)
            name = re.sub(ext, '', i)

            try:
                entry = self.project[name]
                if entry.check_mtime():
                    self.read(path, name)
            except:
                self.read(path, name)


    def read(self, path, name = None, passable = True):
        xml = bacch.read_xml(path)
        if xml is None:
            bacch.log.critical("Unable to read %s" % path)
            if not passable:
                bacch.exit(1)
        elif not passable:
            return xml
        else:
            self.project[name] = bacch.DataEntry(name, path, xml)


    def sync(self):
        return bacch.args.sync

    def update(self):
        self.read_files()

    def fetch(self):
        return self.project
