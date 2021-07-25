from distutils.core import setup

import pathlib
import re

# Configure Packages
packages = [
    "bacch",
    "bacch.commands",
    "bacch.tex"
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
    version="2021.1",
    scripts=scripts,
    package_dir=package_dirs,
    packages=packages,
)

