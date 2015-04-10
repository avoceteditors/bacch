# bacch

`bacch` provides a series of utilities to assist writers working in unix-like environments, such as Linux and FreeBSD.  These utilities include presentation, project statistics, and development tools.  It runs on Python 3 and requires Sphinx and lxml for document processing.



## Current Development

**Version 0.1**

Feature Goals:

- **Project Builder**: System to process source code written reStructuredText/XML to produce HTML, Word documents and PDF's in various formats.

- **Structure Reader**: Similar to the project builder, this outputs as JSON file that indicates the hierarchical organization of source files, based on toctrees and xincludes.

- **Installation**: Project requires some form of packaging and installation system, so that it can easily be installed on any given system.

There is no development schedule or fixed release cycle.  It'll be done when it's done.

## Release Notes

### Version 0.x

Initial development releases.

#### Version 0.3

First version to successfully run build system top to bottom on a project written in reStructuredText.  Provides configuration options for minor adjustments in formatting.


#### Version 0.2

Developed the `bacchbuilder` Sphinx extension.  When Sphinx is called by itself, able to create a properly formatted PDF document of a novel for trade paperback release. 

#### Version 0.1

First prototype `bacch` system.  `bacch` able to successfully parse XML source code to produce a single HTML document.

