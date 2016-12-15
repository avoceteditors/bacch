# Module Imports
import logging

# Log Handler
class LogHandler():

    def __init__(self, args):
        
        # Initialize Logging Level
        if args.debug:
            loglevel = logging.DEBUG
        else:
            loglevel = logging.INFO

        # Set Logfile Path
        logfile = args.logfile

        logging.basicConfig(
            filename = logfile,
            level = loglevel,
            format = '[Bacch %(levelname)s  -  %(asctime)s]: %(message)s')

    
# Verbose Handler
class VerboseLogHandler(LogHandler):

    # Log Debug
    def debug(self, msg):
        print('DEBUG:    %s' % msg)
        logging.debug(msg)

    # Log Info
    def info(self, msg):
        print('INFO:     %s' % msg)
        logging.info(msg)

    # Log Warning
    def warn(self, msg):
        print('WARNING:  %s' % msg)
        logging.warning(msg)
        
    # Log Error
    def error(self, msg):
        print('ERROR:    %s' % msg)
        logging.error(msg)

    # Log Critical
    def critical(self, msg):
        print('CRITICAL: %s' % msg)
        logging.critical(msg)


# Quiet Handler
class QuietLogHandler(LogHandler):

    # Log Debug
    def debug(self, msg):
        logging.debug(msg)

    # Log Info
    def info(self, msg):
        logging.info(msg)

    # Log Warning
    def warn(self, msg):
        logging.warning(msg)
        
    # Log Error
    def error(self, msg):
        logging.error(msg)

    # Log Critical
    def critical(self, msg):
        logging.critical(msg)
