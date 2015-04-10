# bacch

Do you like to write?  Do you do your writing in a unix-like environment -- such as Linux, FreeBSD and Mac OS X? `bacch` provides a command-line build system for writers, especially novelists, looking to move away from the cumbersome feature bloat of word processors into a more streamlined plain text markup-based workflow.

In particular, `bacch` separates the writing process from typesetting concerns, so you can focus on the text without the distraction of how it looks and without losing the ability to share quality PDF's for presentation and distribution purposes.  The build system is an extension on existing technologies current used in software documentation, adapted for the fiction writer with an eye towards simplifying setup, use and configuration.

It is written in Python 3.4.3 and requires Sphinx, lxml and LaTeX.

## Current Development

For the time being, `bacch` remains in active development.  The following features are targets for the next version:

- **XML Support**: Target for nonfiction writers.  Requires framework to be set up in the main program and an XSLT stylesheet written to port the LaTeX converter for Sphinx over to XML.

- **Standard Manuscript Format**: For the moment, `bacch` only provides proper formatting for trade paperback.  This would allow a single command to format the document for mailing to a publisher.

- **Additional Markup**: Fine tuning in the LaTeX to support notes, todos, footnotes, endnotes, and other Sphinx and XML elements.  Some of these will need additional configurations to allow the user to hide them from display.

- **Deprecate conf.py**: Sphinx normally requires `conf.py` to set default configurations for its run, but conf.py is needlessly complex and not compatible with the XML reader.  More importantly, if certain configuration values aren't set the build fails. Using the `-C` argument disables the `conf.py` reading, allowing values to be set wholly through `-D`.  Adapt the call system to remove the need, moving the user down to project.conf.

- **Default System**: The argument defaults at the moment are handled through the Sphinx module.  Move this to the main program class where it'll make for easier reference.

- **Structural Reader**: Requires an adaptation of the builder to create a reference file in the project root that shows the structure of the project in JSON.  Necessary for future feature goals.

- **Package Support**: System to automate the installation and update process.

For the moment, there is no development schedule for this project, but all these features and a few more besides are necessary before it advances to version 1.x.


## Explanation of the Name

The program is developed under the label Dionysiac Endeavors.  This was chosen with a nod to the dualism Friedrich Nietzsche lays out in his book *The Birth of Tragedy from the Spirit of Music* and to the jazz traditions in music. The root goal of D.E. is to develop tools that facilitate a balance between the two sides.  That is, apollonian approach to enabling and cultivating dionysiac endeavors -- the way a jazz arrangements use structure to accent the improvisation.

The name `bacch` derives from Bacchus, the Roman name for Dionysus.  It facilitates this goal by removing the obsessive tinkering with fonts and page layouts and the tedium of going back and doing it again when something doesn't quite fit.

The entire book's formatting is relegated to the build system, handled through a basic configuration file -- so that the writer's focus can remain fixed instead upon the text.


## Release Notes

### Version 0.x

Initial development releases.

**Version 0.3**: First version to successfully run build system top to bottom on a project written in reStructuredText.  Provides configuration options for minor adjustments in formatting.

**Version 0.2**: Developed the `bacchbuilder` Sphinx extension.  When Sphinx is called by itself, able to create a properly formatted PDF document of a novel for trade paperback release. 

**Version 0.1**: First prototype `bacch` system.  `bacch` able to successfully parse XML source code to produce a single HTML document.

