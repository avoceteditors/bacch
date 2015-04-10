# bacch

`bacch` provides a command-line build system for writers working in unix-like environments -- such as Linux, FreeBSD and Mac OS X.  It allows writers to work on plain text files, using simple markup, to generate quality PDF's for presentation and distribution purposes.

This system extends existing technologies used in documentation writing, with an eye towards simplifying setup, configuration and use.  It is written in Python 3.4.3 and requires Sphinx, lxml and LaTeX, (a complete list of dependencies will be added at a later date).

## Current Development

For the time being, `bacch` remains in active development.  The following features are targets for the next version:

- **XML Support**: Target for nonfiction writers.  Requires framework to be set up in the main program and an XSLT stylesheet written to port the LaTeX converter for Sphinx over to XML.

- **Standard Manuscript Format**: For the moment, `bacch` only provides proper formatting for trade paperback.  This would allow a single command to format the document for mailing to a publisher.

- **Additional Markup**: Fine tuning in the LaTeX to support notes, todos, footnotes, endnotes, and other Sphinx and XML elements.  Some of these will need additional configurations to allow the user to hide them from display.

- **Deprecate conf.py**: Sphinx normally requires `conf.py` to set default configurations for its run, but conf.py is needlessly complex and not compatible with the XML reader.  More importantly, if certain configuration values aren't set the build fails. Using the `-C` argument disables the `conf.py` reading, allowing values to be set wholly through `-D`.  Adapt the call system to remove the need, moving the user down to project.conf.

- **Default System**: The argument defaults at the moment are handled through the Sphinx module.  Move this to the main program class where it'll make for easier reference.

- **Structural Reader**: Requires an adaptation of the builder to create a reference file in the project root that shows the structure of the project in JSON.  Necessary for future feature goals.

- **Package Support**: System to automate the installation and update process.


## An Explanation of the Name

The program is being developed under the label Dionysiac Endeavors.  This label was chosen with a nod to the dualism of Friedrich Nietzsche in his work *The Birth of Tragedy* and the traditions of jazz.  To develop a structural apolline approach or arrangement that allows for greater improvisation and other cultivations of dionysiac influences in the work.

`bacch` derives from Bacchus, the Roman name for Dionysus.


## Release Notes

### Version 0.x

Initial development releases.

**Version 0.3**: First version to successfully run build system top to bottom on a project written in reStructuredText.  Provides configuration options for minor adjustments in formatting.

**Version 0.2**: Developed the `bacchbuilder` Sphinx extension.  When Sphinx is called by itself, able to create a properly formatted PDF document of a novel for trade paperback release. 

**Version 0.1**: First prototype `bacch` system.  `bacch` able to successfully parse XML source code to produce a single HTML document.

