#!/usr/bin/env python3

from setuptools import setup, find_packages
from os.path import join

setup(name = 'bacch',
    version = '0.14',
    entry_point = {
        'sphinx.builders': {
            'bacch': 'bacch.sphinx',
            'gnomon': 'bacch.sphinx'
        }
    },
    packages = find_packages(exclude=['tests']) 
)
