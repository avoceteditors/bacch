# bacch

`bacch` provides a build system for novelists working in unix-like environments, such as Linux and FreeBSD.  It allows the writer to work in simple markup languages, keeping the writing process separate from formatting and typesetting concerns. It adapts and improves upon existing technologies typically used only in software documentation.  Its goal is to simplify these tools, making it easier to set up projects and format the final document.

It is written in Python 3.4.3 and uses Sphinx 1.2.3, lxml and LaTeX.  It supports reStructuredText and DocBook XML as source formats.


## Current Development

For the time being, `bacch` remains in active development.  The following features are targets for the next version:

- **XML Support**: Target for nonfiction writers.  Requires framework to be set up in the main program and an XSLT stylesheet written to port the LaTeX converter for Sphinx over to XML.

- **Standard Manuscript Format**: For the moment, `bacch` only provides proper formatting for trade paperback.  This would allow a single command to format the document for mailing to a publisher.

- **Additional Markup**: Fine tuning in the LaTeX to support notes, todos, footnotes, endnotes, and other Sphinx and XML elements.  Some of these will need additional configurations to allow the user to hide them from display.

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

