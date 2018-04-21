#!/usr/bin/env python3

from setuptools import setup
from os.path import join

setup(name = 'bacch',
    version = '0.13',
    entry_point = {
        'sphinx.builders': {
            'bacch': 'bacch.sphinx',
            'gnomon': 'bacch.sphinx'
        }
    },
    packages = ['bacch'],
)
