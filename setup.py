
#!/usr/bin/env python3
from setuptools import setup

setup(name = 'bacch',
        version = '0.11',
        author = 'Kenneth P. J. Dyer',
        author_email = 'kenneth@avoceteditors.com',
        url = 'https://github.com/avoceteditors/bacch',
        description = "A document generator",
        license = 'BSD 3-clause',
        packages = ['bacch'],
        scripts = ['scripts/bacch'],
        install_requires = [],
        classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Topic :: Text Processing :: Markup'],
)
