# Bacch

Do you like to write?  Do you do your writing in a unix-like environment -- such as Linux, FreeBSD or Mac OS X?  Bacch provides an extension for the Sphinx documentation build system for writers working with print documents, especially novelists looking to move away from the cumbersome feature-bloat of word processors into a more streamlined plain text markup-based workflow.

The aim of Bacch is to help separate the writing process from typesetting concerns, so you can focus on the story without the distraction of how it looks and without losing the ability so share quality PDF's for presentation and distribution purposes.

## Current Development

For the time being, Bacch remains in active development, certain parts may or may not work in production.  The following features are targets for the next version:

- **Standard Manuscript Format**: For the moment, `bacch` only provides proper formatting for trade paperback.  This would allow a single command to format the document for mailing to a publisher.

- **Additional Markup**: Fine tuning in the LaTeX to support notes, todos, footnotes, endnotes, and other Sphinx and XML elements.  Some of these will need additional configurations to allow the user to hide them from display.

- **Structural Reader**: Requires an adaptation of the builder to create a reference file in the project root that shows the structure of the project in JSON.  Necessary for future feature goals.

- **Package Support**: System to automate the installation and update process.

- **Initialization Script**: Requires new script to replace `sphinx-quickstart`, generating a default `conf.py` and `Makefile`.

For the moment, there is no development schedule for this project, but all these features and a few more besides are necessary before it advances to version 1.x.


## Explanation of the Name

The program is developed under the label Dionysiac Endeavors.  This was chosen with a nod to the dualism Friedrich Nietzsche lays out in his book *The Birth of Tragedy from the Spirit of Music* and to the jazz traditions in music. The root goal of D.E. is to develop tools that facilitate a balance between the two sides.  That is, apollonian approach to enabling and cultivating dionysiac endeavors -- the way a jazz arrangements use structure to accent the improvisation.

The name Bacch derives from Bacchus, the Roman name for Dionysus.  It facilitates this goal by removing the obsessive tinkering with fonts and page layouts and the tedium of going back and doing it again when something doesn't quite fit.

The entire book's formatting is relegated to the build system, handled through a basic configuration file -- so that the writer's focus can remain fixed instead upon the text.


## Release Notes

### Version 0.x

Initial development releases.

**Version 0.4**: After some deliberation chose to transition the project from a standalone application to a Sphinx module.  Stripped out the `bacch.py` wrapper, created a new version of `bacchbuilder.py` and `bacchwriter.py` for the Sphinx components, with new `bacch.py` now relegated to the initializing the builder.  For the moment, plans for XML support abandoned.

**Version 0.3**: First version to successfully run build system top to bottom on a project written in reStructuredText.  Provides configuration options for minor adjustments in formatting.

**Version 0.2**: Developed the `bacchbuilder` Sphinx extension.  When Sphinx is called by itself, able to create a properly formatted PDF document of a novel for trade paperback release. 

**Version 0.1**: First prototype `bacch` system.  `bacch` able to successfully parse XML source code to produce a single HTML document.

