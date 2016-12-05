# Module Imports
import datetime
import os
import os.path
import sys
import bacch


# Main Process
def run(args):
    """ Main Control Function.

    Receives command-line arguments (argparse) then runs
    the Bacch the main process.  Intended primarily for
    use by the ``bacch`` command script.
    """

    ######################
    # Initialize Timer
    time_start = datetime.datetime.now()

    ######################
    # Masthead
    name = "Bacch"
    slogan = "The Document Generator"
    version = "0.7"

    if args.verbose:
        content = [
            '%s: %s' % (name, slogan),
            'Kenneth P. J. Dyer',
            'kenneth@avoceteditors.com',
            'Version %s' % version,
            ''
        ]
        masthead = '\n  '.join(content)
    else:
        masthead = '%s - version %s\n' % (name, version)

    print(masthead)

    ######################
    # Switch to Working Directory
    if args.wdir is not None:
        if os.path.isdir(args.wdir):
            os.chdir(args.wdir)

    ######################
    # Reader
    read = bacch.Reader(args)


    ######################
    # Builder
    if args.build is not None:
        conf, build = bacch.builder(read)

        # Writer
        for tree in build:
            writer = bacch.Writer(read, tree, conf)
            writer.write()

    ######################
    # Exit
    time_end = datetime.datetime.now()
    time_diff = time_end - time_start
    count = round(time_diff.total_seconds(), 2)
    msg = 'Operation completed in %s seconds' % count
    print(msg)
    sys.exit(0)



############################
# Fetch Namespace from Element
def getns(element):

    print(element.tag)
    return 'yes'
