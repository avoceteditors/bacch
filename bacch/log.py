# Module Imports
import logging
import os.path

class Log():

    def __init__(self, config):
        self.config = config
        
        self.debug_status = config['ARGS']['debug']
        self.verbose = config['ARGS']['verbose']

        if self.debug_status:
            loglevel = logging.DEBUG
        else:
            loglevel = logging.WARNING

        path = os.path.join(
                config['SYSTEM']['tmp'],
                config['SYSTEM']['log'])
        logging.basicConfig(
            filename = path,
            level = loglevel,
            format = '[ Bacch %(levelname)s ][ %(asctime)s ]: %(message)s'
        )


    def debug(self, msg):
        logging.debug(msg)

        if self.verbose:
            print('DEBUG:    %s' % msg)

    def info(self, msg):
        logging.info(msg)

        if self.verbose:
            print('INFO:     %s' % msg)


    def warn(self, msg):
        logging.warning(msg)

        if self.verbose:
            print('WARN:     %s' % msg)



    def error(self, msg):
        logging.error(msg)

        if self.verbose:
            print('ERROR:    %s' % msg)


    def critical(self, msg):
        logging.critical(msg)

        if self.verbose:
            print('CRITICAL: %s' % msg)

