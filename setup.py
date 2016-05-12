
#!/usr/bin/env python3
from distutils.core import setup
import sys
import os.path
import site

bacch_description = "Document processor for fiction and nonfiction book writers, based on Sphinx."
lib = site.USER_SITE
config = os.path.join(lib, 'bacch', 'config')

setup(name = 'bacch',
        version = '0.6',
        author = 'Kenneth P. J. Dyer',
        author_email = 'kenneth@avoceteditors.com',
        url = 'https://github.com/avoceteditors/bacch',
        description = bacch_description,
        license = 'BSD 3-clause',
        packages = ['bacch'],
        scripts = ['scripts/bacch'],
        classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Topic :: Text Processing :: Markup'],
        data_files = [
            (config,
             ['config/main.conf']
             )]
)
