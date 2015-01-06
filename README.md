# bacch

`bacch` provides a series of utilities to assist writers working in unix-like environments, such as Linux and FreeBSD.  These utilities include presentation, project statistics, and development tools.  It requires Python 3 and the Sphinx documentation builder.



## Current Development

**Version 0.1** is in active development.  This is the initial version for the project, as such there is no stable branch available.  For the time being you should not use anything in this repo as it either doesn't work or doesn't do anything.

*Note*: For the present, the author can only perform testing in Linux and would appreciate comment on any problems that arise on FreebSD.  Preferably comment that can point to the why and how.

Feature Goals:

- **Project Builder**: Develop a simplified call system for generate presentation documents from source code.  For this version, focus on implementing the Sphinx build system with HTML output.  Assume that the source directory contains a `conf.py` file, but prepare for when it doesn't.

- **Project Updater**: Develop a parser for source files.  This system should read all files in the source directory, sort them based on logical structure noting any files that do not fit into the TOC tree, then create a JSON file at the project root.  For this version focus on reading source files in reStructuredText.

- **Installation Script**: Develop an installation script that users can run to update their systems with the newest version of bacch.  This system should copy relevant files to their expected locations, (id est, configs to `/etc`, modules to `/usr`, et cetera).  It should also create or update the launch script in `/usr/bin` where necessary.

There is no development schedule or fixed release cycle.  There is only one developer on this project and it is undertaken to address his specific needs as a technical writer and aspirant novelist.  When the above features are implemented and stable, it will be noted here and branches created for the next version.

## Release Notes

None.  Nothing is yet stable.

