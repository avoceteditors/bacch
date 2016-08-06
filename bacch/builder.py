##########################################################################
# Module Imports
from bacch import core as bacch_core

##########################################################################
# Builder Class
class Builder():

    # Initialize Class
    def __init__(self, config, reader):
        self.config = config
        self.reader = reader


        build = self.config.build
        builders = self.config.system_builders

        if build in builders:
            self.buildconf = getattr(self.config, 'build_%s' % build)
            self.format = self.buildconf.format

            # Check Format
            if self.format.lower() == 'pdf':
                self.transform = PDFTransformer
            else:
                bacch_core.log(self.config.verbose, 'critical',
                        'Bacch does not currently support %s output.' % self.format)
        else:
            self.buildconf = self.config.build_default
