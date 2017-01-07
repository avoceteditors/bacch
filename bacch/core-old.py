"""
This module provides the core functions for Bacch,
including the main `run()` and `exit()` processes.
"""

# Module Imports
import datetime
import sys
import os
import bacch


###################
# Exit Bacch
def exit(exit_code, stats = None):
    """ This function provides the exit process.

    It takes an exit code integer and a stats dictonary
    as arguments.  If stats is not None and args.verbose
    is True, it reports on operation stats.  Otherwise,
    it prints the time it took to run then exits, passing
    the exit code to sys.exit().
    """

    # Compile and Report Stats
    msgs = []
    if stats is not None and bacch.args.verbose:
        files_read = 'Files:\t%s' % stats['files']
        msgs.append(files_read)

        print("\nStatistics")
        for i in msgs:
            print(' - %s' % i)

    # Time Report
    time_end = datetime.datetime.now()
    time_diff = time_end - bacch.time_start
    sec = round(time_diff.total_seconds(), 2)
    close_msg = '\nOperation completed in %s seconds' % sec
    print(close_msg)

    # Exit
    sys.exit(exit_code)

###################
# Create Directory 
def makedir(path):
    """ Creates a direcotry in the event that it does
    not already exist.
    """
    if not os.path.exists(path):
        os.mkdir(path)
    elif os.path.isfile(path):
        bacch.log.critical('Invalid Directory Path (isFile): %s' % path)
        sys.exit(1)

   
###################
# Main Process
def run(args):
    """ Function handles the main application process.
    """

    ###################
    # Init Bacch
    time_start = datetime.datetime.now()
    setattr(bacch, 'time_start', time_start)

    # Store Args
    setattr(bacch, 'args', args)

    ###################
    # Masthead
    if args.verbose:
        content = [
            '%s - %s' % (bacch.__name__, bacch.__slogan__),
            bacch.__author__,
            bacch.__author_email__,
            'Version %s' % bacch.__version__, '']
        masthead = '\n  '.join(content)
    else:
        masthead = '%s - version %s' % (bacch.__name__, bacch.__version__)

    print(masthead)

    ###################
    # Set Working Directory
    try:
        work = args.working_dir
        os.chdir(work)
    except:
        work = os.getcwd()
        
    # Set Sync
    setattr(bacch, 'sync', args.sync)
    
    ###################
    # Init Log Handler
    if args.verbose:
        log = bacch.VerboseLogHandler(args)
    else:
        log = bacch.QuietLogHandler(args)
    setattr(bacch, 'log', log)

    ####################
    # Starting Bacch
    bacch.log.info('Starting Bacch')
    bacch.log.debug('Working Directory: %s' % os.path.abspath(work))
    bacch.log.debug('Log File: %s' % os.path.abspath(args.logfile))

    # Directory Structure
    bacch.log.debug("Initializing Directory Structure")
    configdir = '.bacch'
    tmp = os.path.join(configdir, 'tmp')
    pick = os.path.join(configdir, 'pickle')
    dirs = [configdir, tmp, pick]

    for i in dirs:
        makedir(i)

    # Data Handler
    pickle_path = os.path.join(pick, 'bacch.pickle')
    datahandler = bacch.load_data(pickle_path)
    
    ###################
    # Build Project
    bacch.log.info("Initialize Builder")
    builds = datahandler.builds
    build_keys = datahandler.fetch_keys()

    build_default = datahandler.build_default
    build_call = args.build
    if build_call is None:
        call = build_default
    else:
        if build_call in builds:
            call = build_call
        elif build_call in build_keys:
            call = '__FILEBUILD__'
            builds[call]['target'] = build_call
        else:
            bacch.log.error("Invalid Build Call")
            exit(1)

    build = builds[call]
    element = build['element']
    



    ###################
    # Exit

    # Init Exit Stats
    stats = {
        "files": len(datahandler.fetch())
    }
 
    # Save Data Handler
    bacch.save_data(pickle_path, datahandler)
    
    # Run Exit
    exit(0, stats)
