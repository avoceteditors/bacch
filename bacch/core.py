##########################################################################
# Module Imports
import logging
import sys
from bacch import config as bacch_config
from bacch import reader as bacch_reader
from bacch import builder as bacch_builder

##########################################################################
# Main Process Class
class Main():

    # Initialize Class
    def __init__(self, args):

        # Masthead
        name = 'Bacch: The Website & Document Generator'
        version = '0.8'

        if args.verbose or args.version:
            contact = [ '',
                        'Kenneth P. J. Dyer',
                        'Avocet Editorial Consultants',
                        'kenneth@avoceteditors.com',
                        'Version %s' % version, '\n\n']
            masthead = name + '\n   '.join(contact)
        else:
            masthead = ' - version '.join([name, version])


        if args.version:
            sys.exit(masthead)
        else:
            print(masthead)

        # Configure Logging
        logfile = args.log
        loglevel = args.log_level
        logging.basicConfig(level = getattr(logging, loglevel.upper()),
                filename = logfile,
                format = '[%(asctime)s][%(levelname)s][Bacch]: %(message)s')

        log(args, 'info', 'Starting Bacch')


        # Configure Bacch
        log(args.verbose, 'info', 'Configuring Bacch')
        bacchconf = bacch_config.Config(args)
        config = bacchconf.get_config()
        log(args.verbose, 'info', 'Configuration Complet')

        # Read Project
        log(args.verbose, 'info', 'Reading Project')
        reader = bacch_reader.Reader(config)
        log(args.verbose, 'info', 'Read Complete')

        # Call Builder
        log(args.verbose, 'info', 'Building Project')
        builder = bacch_builder.Builder(config, reader)
        log(args.verbose, 'info', 'Build Complete')

##########################################################################
# General Functions

# Logging Function
def log(arg, level, msg):

    if level == 'debug':
        level = 'DEBUG'
        logging.debug(msg)
    elif level == 'info':
        level = 'INFO'
        logging.info(msg)
    elif level == 'warn':
        level = 'WARNING'
        logging.warning(msg)
    elif level == 'error':
        level = 'ERROR'
        logging.error(msg)
    elif level == 'critical':
        level = 'CRITICAL'
        logging.critical(msg)

    # Verbose
    if arg:
        print("[%s]: %s" % (level, msg))


