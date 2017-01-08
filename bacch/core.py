"""
This module provides the main processes and core functionality for Bacch.
"""

# Module Imports
import datetime
import sys
import os
import pickle
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
    bacch.__log__.debug("Calculating runtime duration...")
    time_end = datetime.datetime.now()
    time_diff = time_end - bacch._time_start
    sec = round(time_diff.total_seconds(), 2)
    bacch.__log__.debug("Done")
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

    bacch.__log__.debug("Checking Path: %s" % path)
    if not os.path.exists(path):
        bacch.__log__.debug("Path does not exist, creating...")
        os.mkdir(path)
        bacch.__log__.debug("Done")
    elif os.path.isfile(path):
        bacch.__log__.critical("Invalid Directory Path: %s" 
            % path)
        sys.exit(1)
    else:
        bacch.__log__.debug("Path Found.")

##########################################
# Pickle Handlers

# Load Saved Data
def load_data(path):
    """ This function returns bacch.reader.Reader() class.

    When Bacch closes, it saves a pickle of this class in
    .bacch/pickle/bacch.pickle.  If this file does not
    exist, or if Bacch is run with the --force argument,
    it creates a new instance of the class and returns it.

    If the file does exist, it loads the object and calls
    the update() method if it was run with the --sync
    argument.

    If it encounters an error while loading the pickle or
    if it successfully loads the pickle and finds that
    the stored version of master.xml is older than the
    one in the file, it creates and returns a fresh
    instance of the Reader() class.
    """
    bacch.__log__.info("Searching for Saved Read...")

    # Check that Pickle Exists
    if os.path.exists(path) and not bacch.__args__.force:
        
        try:
            # Open Pickle File 
            f = open(path, 'rb')
            reader = pickle.load(f)
            f.close()
        except:
            msg = [
                'Bacch encountered an error while loading',
                'the saved read from the last time it ran.',
                'Creating a new read object.']
            msg = ' '.join(msg)
            bacch.__log__.debug(msg)
            return bacch.Reader()

        # Sync Reader
        if reader.master_updated():
            return bacch.Reader()
        elif bacch.__args__.sync: 
            bacch.__log__.info("Updating File Reads...")
            reader.update()
            bacch.__log__.debug("Reads updated.")

        return reader
        
    # Create New Reader Object
    else:
        bacch.__log__.debug("No Saved Data Found, building...")
        return bacch.Reader()

# Save Pickled Data
def save_data(path, data):
    """ This method saves bacch.reader.Reader() for later use.
    """
    bacch.__log__.info("Saving Data...")

    try:
        # Dump Data to File
        f = open(path, 'wb')
        pickle.dump(data, f)
        f.close()
    except:
        bacch.__log__.warn("Error encountered while saving reader to file.")

##########################################
# Main Process
def run(args):
    """ This function defines the main application process."""

    ######################
    # Initialize Bacch
    time_start = datetime.datetime.now()
    setattr(bacch, '_time_start', time_start)

    # Store Arguments
    setattr(bacch, '__args__', args) 

    ######################
    # Masthead
    if bacch.__args__.verbose:
        content = [
            '%s - %s' % (bacch.__name__, bacch.__slogan__),
            bacch.__author__,
            bacch.__author_email__,
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
        % os.path.abspath(bacch.__args__.logfile))

    # Initialize Directory Structure
    bacch.__log__.debug('Initialize Directory Structure...')
    configdir = os.path.join(
        os.getcwd(), '.bacch')
    tmp     = os.path.join(configdir, 'tmp')
    pickle  = os.path.join(configdir, 'pickle')

    for directory in [configdir, tmp, pickle]:
        makedir(directory)    


    ######################
    # Reader Processes
    picklepath = os.path.join(pickle, 'bacch.pickle')
    reader = load_data(picklepath) 

    ######################
    # Exit Process

    # Save Data
    save_data(picklepath, reader)

    # Close Bacch
    exit()





