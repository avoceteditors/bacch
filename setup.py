from distutils.core import setup

import pathlib
import re

# Configure Packages
packages = [
    "bacch",
]
package_dirs = {}
exts = []
for package in packages:
    src = re.sub("\.", "/", package)
    package_dirs[package] = src

# Configure Scripts
scripts_path = pathlib.Path("scripts")
scripts = []
for i in scripts_path.glob('*'):
    if i.is_file():
        scripts.append(str(i))

setup(
    name="bacch",
    version="2022.1",
    packages=packages,
    entry_point={
        "sphinx.builders": {
            "bacch": "bacch.sphinx"
        }
    }
)

