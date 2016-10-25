# Moduel Imports
import datetime
import sys
import logging

import bacch.docker


# Run Main Process
def run(args):

    # Initialize Bacch
    time_start = datetime.datetime.now()

    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    logging.basicConfig(
        filename = "bacch.log",
        level = loglevel
    )
    logging.info("Starting Bacch")

    ######################
    # Masthead
    name = 'Bacch - The Document Generator'
    version = '0.10'

    if args.verbose:
        content = [
                name,
                'Kenneth P. J. Dyer',
                'Avocet Editorial Consultants',
                'kenneth@avoceteditors.com',
                'Version %s' % version, '']
        masthead =  '\n  '.join(content)
    else:
        masthead = ' - version '.join([name, version])

    print(masthead)

    # Exit Bacch
    time_end = datetime.datetime.now()
    time_diff = time_end - time_start
    sec = round(time_diff.total_seconds(), 2)
    msg = 'Operation completed in %s seconds' % sec
    print(msg)
    sys.exit(0)
    

