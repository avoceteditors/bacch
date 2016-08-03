##########################################################################
# Module Imports
import logging
import sys


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


##########################################################################
# General Functions

# Logging Function
def log(args, level, msg):

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
    if args.verbose:
        print("[%s]: %s" % (level, msg))


