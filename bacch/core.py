# Moduel Imports
import datetime
import sys
import os
import os.path

import bacch.config
import bacch.log
import bacch.project

##########################################
# Helper Functions
def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

##########################################
# Run Main Process
def run(args):

    # Initialize Bacch
    time_start = datetime.datetime.now()

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

    #########################
    # Configure Bacch
    config = bacch.config.configure(args)
    if args.update_config:
        sys.exit(0)

    # Init Paths
    paths = ['.bacch',
        os.path.join('.bacch', 'tmp'),
        os.path.join('.bacch', 'pickle')
    ]
    for i in paths:
        mkdir(i)

    # Init Log
    log = bacch.log.Log(config)
    log.info("Starting Bacch")

    #########################
    # Load Data
    log.info("Initializing project read.")
    path_pickle = os.path.join('.bacch', 'pickle', 'bacch.pickle')
    data = bacch.project.load(config, log, path_pickle)

    #########################
    # Exit Bacch
    time_end = datetime.datetime.now()
    time_diff = time_end - time_start
    sec = round(time_diff.total_seconds(), 2)
    msg = 'Operation completed in %s seconds' % sec
    print(msg)
    sys.exit(0)
    

