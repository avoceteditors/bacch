"""
This module provides the main processes and core functionality for Bacch.
"""

# Module Imports
import datetime
import sys
import os
import bacch

##########################################
# Exit Bacch
def exit(exit_code = 0):
    """ This function provides exit functionality for process.

    It takes an exit code, which is set to 0 by default for 
    clean exits.  It also pulls from the main bacch module
    in order to collect relevant stats for exit messages.
    """

    # Log Time
    bacch.log.debug("Calculating runtime duration...")
    time_end = datetime.datetime.now()
    time_diff = time_end - bacch.time_start
    sec = round(time_diff.total_seconds(), 2)
    bacch.log.debug("Done")
    msg = "\nOperation completed in %s seconds" % sec
    print(msg)

    # Exit
    sys.exit(exit_code)

##########################################
# Make Directory
def makedir(path):
    """ This function checks whether a directory exists.
    If the path does not exist already, it creates it for
    you."""

    bacch.log.debug("Checking Path: %s" % path)
    if not os.path.exists(path):
        bacch.log.debug("Path does not exist, creating...")
        os.mkdir(path)
        bacch.log.debug("Done")
    elif os.path.isfile(path):
        bacch.log.critical("Invalid Directory Path: %s" % path)
        sys.exit(1)
    else:
        bacch.log.debug("Path Found.")


##########################################
# Main Process
def run(args):
    """ This function defines the main application process."""

    ######################
    # Initialize Bacch
    time_start = datetime.datetime.now()
    setattr(bacch, 'time_sart', time_start)

    # Store Arguments
    setattr(bacch, '__args__', args) 

    ######################
    # Masthead
    if bacch.__args__.verbose:
        content = [
            '%s - %s' % (bacch.__name__, bacch.__slogan__),
            bacch.__author__,
            bacch.__email__,
            'Version %s' % bacch.__version__,'']
        masthead = '\n  '.join(content)
    else:
        masthead = '%s - version %s' % (
            bacch.__name__, bacch.__version__)
    print(masthead)

    ######################
    # Set Working Directory
    try:
        work = bacch.__args__.working_dir
        os.chdir(work)
    except:
        work = os.getcwd()

    ######################
    # Log Handler
    if bacch.__args__.verbose:
        log = bacch.VerboseLogHandler()
    else:
        log = bacch.QuietLogHandler()
    setattr(bacch, '__log__', log)
    
    ######################
    # Starting Bacch
    bacch.__log__.info('Starting Bacch')
    bacch.__log__.debug('Working Directory: %s'
        % os.path.abspath(work))
    bacch.__log__.debug('Log File: %s'
        % os.path.abspath(bacch.__args__.logfile)

    # Initialize Directory Structure
    bacch.__log__.debug('Initialize Directory Structure...')
    configdir = '.bacch'
    tmp     = os.path.join(configdir, 'tmp')
    pickle  = os.path.join(configdir, 'pickle')

    for directory in [configdir, tmp, pickle]:
        makedir(directory)    


    ######################
    # Reader Processes
    picklepath = os.path.join(pickle, 'bacch.pickle')
    bacch.__args__._picklepath = picklepath
    reader = bacch.reader()

    ######################
    # Exit Process

    # Close Bacch
    exit()





