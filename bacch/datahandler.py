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
        bacch.log.info('Configure Project')
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

        # Builds
        base_builds = bacch.fetch_element(self.master, '%s/bacch:builds' % config)[0]
        attr = base_builds.attrib
        try:
            output = attr['output']
        except:
            output = '.'

        self.builds = {}
        default = None
        for build in base_builds:
            attr = build.attrib

            self.builds[attr['id']] = {
                'path': os.path.join(output, attr['path']),
                'element': attr['element'],
                'format': attr['format']
            }
            if default is None:
                default = attr['id']

        self.build_default = default

        # Initialize Page Build
        if '__FILEBUILD__' not in self.builds:
            self.builds['__FILEBUILD__'] = {
                'path': output,
                'element': '%',
                'format': 'html'
            }

        # [[ add block config ]]                

       
        # Read Files
        self.project = {} 
        self.read_files()

        
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

    def fetch_keys(self):
        return self.project.keys()
