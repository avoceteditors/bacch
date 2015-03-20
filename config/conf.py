#! /usr/bin/env python3

################################
# Module Imports
import sys, os, os.path



##################################
# General Configurations

sys.path.insert(0,'/home/kbapheus/repos/bacch/')

# Sphinx Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'bacchbuilder'
]
title = "untitled"
# Templates
templates_path = ['_templates']

# Source Extension
source_suffix = '.rst'

# Source Encoding
source_encoding = 'utf-8'

# Master File
master_doc = 'index'



# Bacch Configurations
bacch_title = "untitled"
bacch_frenchspacing = True
bacch_novel = True