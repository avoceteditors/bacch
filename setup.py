#! /usr/bin/env python3

# Imports
import os
from setuptools import setup



def read(*paths):
    """ Build a file path from *paths* and return contents """
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name = 'bacch',
    version = '0.1.0',
    description = "Writers utilities for tech/fiction work in unix-like environments",
    long_description = ( read('README.md')),
    url = 'https://github.com/kennethpjdyer/bacch/',
    license = read('LICENSE'),
    author = 'Kenneth P. J. Dyer',
    py_modules = [ 'bacch' ],
    include_package_data = True, 
    classifiers = [ ],
)

    

