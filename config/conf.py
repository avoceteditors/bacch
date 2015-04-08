#! /usr/bin/env python3

################################
# Module Imports
import sys, os, os.path

###############################
# bacch Configurations

bacch_sourcedir = '~/repos/bacch/'
sys.path.insert(0,bacch_sourcedir)

# Sphinx Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'bacchbuilder',
    'bacchbuilder-new']

# Templates
templates_path = ['_templates']

# Source Extension
source_suffix = '.rst'

# Source Encoding
source_encoding = 'utf-8'

# Master File
master_doc = 'index'





