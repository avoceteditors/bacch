# Module Imports
import datetime
import sys
import os
import bacch


###################
# Exit Bacch
def exit(exit_code):
    time_end = datetime.datetime.now()
    time_diff = time_end - bacch.time_start
    sec = round(time_diff.total_seconds(), 2)
    close_msg = '\nOperation completed in %s seconds' % sec
    print(close_msg)
    sys.exit(exit_code)

def makedir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    elif os.path.isfile(path):
        bacch.log.critical('Invalid Directory Path (isFile): %s' % path)
        sys.exit(1)

   
###################
# Main Process
def run(args):

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
    
    if element == "*" or element == '%':
        builder = bacch.PageBuilder(build, datahandler)
        bacch.log.info('Page Builder: Ready')
    else:
        builder = bacch.BookBuilder(build, datahandler)
        bacch.log.info('Book Builder: Ready')

    # Writer
    bacch.log.info('Initialize Writer')
    writer_type = build['format']
    if writer_type == 'html':
        writer = bacch.HTMLWriter(build, builder, datahandler)
        bacch.log.info('HTML Writer: Ready')
    elif writer_type == 'latex':
        writer = bacch.LATEXWriter(build, builder, datahandler)
        bacch.log.info('LaTeX Writer: Ready')
    else:
        bacch.log.error("Invalid Writer Format: %s" % writer_type)
        exit(1)

    writer.parse()



    ###################
    # Exit
    exit(0)

           
    
        
    

