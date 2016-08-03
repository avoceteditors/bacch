##########################################################################
# Module Imports
import configparser
import os.path

from bacch import core as bacch_core


##########################################################################
# Configuration Class
class Config():

    # Initialize Class
    def __init__(self, args):
        self.args = args

        # Parse Configuration Files
        self.config = self.set_configs()


    # Define Configuration Options
    def set_configs(self):
        
        # Find System Configuration
        config_sys = prototype_config()

        # Find Local Configuration
        localpath = self.args.config

        if os.path.exists(localpath):
            local_config = configparser.ConfigParser()
            local_config.read(localpath)
        else:
            local_config = None

        # Initialize config Object
        config = ConfigObject()

        # Set Base Attributes
        for unit in ["System", "Metadata"]:
            unitname = unit.lower()
            for key in config_sys[unit]:
                parameter = "%s_%s" % (unitname, key)
                try:
                    value = config_local[unit][key]
                except:
                    value = config_sys[unit][key]

                setattr(config, parameter, value)

        # Set Default Build Attributes
        setattr(config, 'build_default', ConfigObject)
        for key in config_sys["Build"]:
            value = config_sys["Build"][key]
            setattr(config.build_default, key, value)


        config.builders = config.system_builders.split(',')
        for build in config.builders:

            # Set Build Name
            setattr(config, 'build_%s' % build, ConfigObject)

            # Load Build Config
            try:
                local = config_local['Build: %s' % build]
            except:
                bacch_core.log(self.args.verbose, 'warn', 
                        "Build %s is invalid, reverting to defaults" % build)
                local = config_sys['Build']

            # Set Configs
            build_conf = getattr(config, 'build_%s' % build)
            for key in config_sys['Build']:
                try:
                    value = local[key]
                except:
                    value = getattr(config.build_default, key)

                setattr(build_conf, key, value)

        return config

    # Fetch Config
    def get_config(self):
        """ Fetch Configuration Object, with CLI Overrides

        This method access the configuration object as defined in the
        set_configs() method and returns it to the control module.  It also
        overrides the existing settings with arguments from the command-line.
        """
        ##########################
        # Command-line Overrides

        # Override Source
        if self.args.source is not None:
            self.config.system_source = self.args.source

        # Override Output
        if self.args.output is not None:
            self.config.system_output = self.args.output

        ###########################
        # Operations
        setattr(self.config, 'update_all', self.args.update)
        setattr(self.config, 'book_build', self.args.book)
        setattr(self.config, 'verbose', self.args.verbose)
        
        build = self.args.build
        if build is None:
            build = self.config.builders[0]
        setattr(self.config, 'build', build) 

        # Nonconfigurable Variables
        setattr(self.config, 'workdir', '.bacch')
        setattr(self.config, 'pickledir', 
                os.path.join('.bacch', 'pickle'))

        return self.config



##########################################################################
# Cos Configuration Object
class ConfigObject():
    """"
    Configuration object, used in storing values for later reference.
    """
    pass


##########################################################################
# General Functions

# Default Config Prototype
def prototype_config():
    """ Provides Default Configuration

    In production, Bacch will read its default configuration options
    from a local or system level file created during installation.
    However, such an implementation would prove distracting during
    early stages of development.  As such, we have created this function,
    which simply returns a dict object with the relevant configs.  Its
    functionality will be deprecated at a later date, but it'll be left
    in place for testing purposes.

    The return dict imitates the configparser read() method, with
    top level units and second level parameters and values.
    """

    # Initialize Config Object
    base_config = {
        "System": {
            "source": "source",
            "output": "output",
            "builders": "Default",
            "extension": "rst"

        },
        "Metadata": {
            "title": "Untitled",
            "author": "Anonymous",
        },
        "Build": {
            "format": "pdf"    
        }
    }

    return base_config