# Module Imports
import bacch
import sys
import re
import lxml.etree as ET

# Compile Doctree
def compile_doctree(config, doctree, data, name = 'master.xml'):

    ns = config['ns']['bacch']
  
    elements = doctree.getchildren()

    if elements != []:
        for element in elements:
            
            # Fetch Data
            if element.tag == "{%s}include" % ns:
                href = element.attrib['href']
                
                try:
                    basetree = data[href].fetch()

                    newtree = compile_doctree(config, basetree, data)
                    doctree.replace(element, newtree)
                except:
                    print("Bad Include href in %s: %s" % (name, href))
            else:
                compile_doctree(config, element, data, name)
    return doctree


# Control Functon
def builder(read):
    """ Function controls the build process.  It determines the type of
    build you want to run and calls and returns the appropriate classes
    to handle that process.
    """
    config = read.fetch_data()['config']
    builds = config['builds']
    args = config['args']

    keys = read.fetch_keys()

    # Determine Builder
    if args.build in builds:
        build_conf = builds[args.build]
    elif args.build in keys:
        print("File found, no builder available.")
    else:
        print("No Builder Found")


    doctree = config['doctree']

    # Separate Elements
    build_element = build_conf['element']
    elements = ['series', 'book', 'chapter', 'section']


    if build_element == "*":

        doctrees = read.fetch_doctrees()

        print(doctrees)
    elif build_element in elements:
        print("Build Element")

        base_doctree = compile_doctree(config, doctree, read.fetch_data()['content'])

        doctrees = base_doctree.xpath('//book:%s' % build_element,
                namespaces = config['ns'])


    return build_conf, doctrees
