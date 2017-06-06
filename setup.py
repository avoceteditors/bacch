#!/usr/bin/env python3

from setuptools import setup

setup(name = 'bacch',
    version = '0.12',
    entry_point = {
        'sphinx.builders': {
            'bacch': 'bacch.book'
        }
    },
    packages = ['bacch']
)
