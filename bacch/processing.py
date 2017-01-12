""" This module provides processing handlers to use in converting
the given lxml doctree into the target format.
"""

# Module Imports
import bacch

# HTML Handler
def htmlHandler(build):
    """ This function handles main and post processing
    for html output. """
    pass

# LaTeX Handler
def latexHandler(build):
    """ This function handles the main and post processing
    for LaTeX output. """
    pass

# Processing Handler
def processingHandlers(reader):
    """ This function provides the main control process for
    the various processors used in converting the lxml doctree
    to the target format. """
    
    bacch.__log__.info('Initializing Processing Modules...')

    # Determine the Builder
    if bacch.__args__.build in reader.builds:
        build_name = bacch.__args__.build
    else:
        keys = reader.builds.keys()
        build_name = sorted(keys)[0]
    
    bacch.__log__.debug("Build Set to: %s" % build_name)    
    build_format = reader.builds[build_name]

    # Preprocessor
    build = bacch.Preprocessor(build_format, reader)

    # Processor
    format_name = build_format['format']
    func = getattr(bacch, '%sHandler' % format_name)

