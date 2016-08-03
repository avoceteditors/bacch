##########################################################################
# Module Imports
import configparser
import os.path

##########################################################################
# Configuration Class
class Config():

    # Initialize Class
    def __init__(self, args):
        self.args = args

        # Parse Configuration Files
        config = self.get_configs()


    # Fetch Configuration Options
    def get_configs(self):
        
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
        config = object

        # Set Attributes
        for unit in config_sys:
            print(unit)



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
            "output": "output"
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
