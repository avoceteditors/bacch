##########################################################################
# Module Imports


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
    which simply returns a dict object with the relevant configs.

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
