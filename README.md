# Bacch


## Introduction

For those who write or want to write longer works, such as books or novels, there are certain limitations to working in traditional wysiwyg environment, such as the word processor.  Typically, these applications are not built to handle multiple related files or to maintain consistent formatting throughout the project.  Documentation writers have long enjoyed various programmatic solutions to these problems and while effective in that capacity, it requires some technical skill in adapting to other purposes.

Bacch extends the Sphinx documentation generator to parse files written in reStructuredText and output a PDF in trade paperback format.  Its purpose is to help separate the writing process from typesetting concerns, so that you can focus on the story without the distraction of how it looks and without losing the ability to share a quality PDF for presentation and distribution purposes.

It is written in Python 3.4.

### Meaning of the Name

The name Bacch derives from a shorten form of Bacchus, whom the Greeks called the god Dionysus.  It is the inaugural production of Dionysiac Endeavors, a name chosen with a nod to the philosopher Friedrich Nietzsche and his work *The Birth of Tragedy from the Spirit of Music*.

Dionysiac Endeavors seek to provide apollonian solutions for writers to better facilitate expressions of the dionysiac in their work.

### Current Development

Bacch remains in active development.  Certain aspects may not work as expected or support all platforms.  Material referenced in this file are subject to change as the work progresses.  The following features are targets of the next few versions:

- **Standard Manuscript Format**: For the moment, Bacch can only compile into trade paperback format.  This is fine for writers that wish to self-publish, but is an obstacle for those who would like to follow the traditional publishing route.

- **Chapter Output**: Instead of creating a single document, Bacch outputs a PDF for each chapter.  This is intended to facilitate the review process.

- **Additional Markup**: Implement formatting for code blocks and inline code, to better facilitate technical writers.  Introduce support for verse blocks and formatting options for verse, such as spacing, caesuras and line numbers, to better facilitate poets.

- **Package Support**: Develop an installation script to automate setting up systems to use Bacch.

- **Initialization Script**: Develop a script to run Sphinx and to initialize a directory structure for new projects.

There is no development schedule for this project.  These features are not being developed in order, but all are considered necessary before beginning version 1.x.


## Using Bacch

In the traditional word processing paradigm, writing and typesetting take place within the same application.  Here they are separate.

You write in a text editor, using the reStructuredText markup language.  Then, when you're ready you run Sphinx calling the Bacch extension to typeset your work, producing a PDF for presentation and distribution purposes.

> **Note**: For the moment, Bacch is actively being used by writers working on the Linux operating system, running Sphinx 1.3.  It probably works without any trouble on FreeBSD and Mac OS X.  It *should* work (but probably does not) on Microsoft Windows.

To run a build, use the following command:

```console
$ sphinx-build -b fullbacch sourcedir builddir
```

This outputs a LaTeX in the build directory.  The file has the same name as the master file. For instance `sourcedir/index.rst` outputs as `builddir/index.tex`.

For the moment, Bacch dos not contain an internal process to convert the LaTeX output into a PDF.  You need to manage this through an external application, such as `pdflatex`:

```console
$ pdflatex --output=builddir --shell-escape builddir/index.tex
```

This in turn creates the final PDF as `builddir/index.pdf`.

>*Note*: `pdflatex` does not properly parse the table of contents with any consistency.  You need to run it a few times in order to get the information arranged properly in the output.  As such, it is recommended that you use `rubber` instead, as it handles this looping for you.

You may find it convenient to create a `Makefile` in the project root to automate these commands, allowing you to build a new PDF using a very brief command:

```console
$ make
```

## Contribution

If you notice a bug, would like to make a suggestion, or have a feature request: create an issue.

## Documentation

### Installation 

Bacch is an extension on Sphinx written in Python 3.4.  To install it, download the repo from GitHub to a location convenient on your system.

```console
$ git pull https://github.com/dionysiac-endeavors/bach
```

Wherever you place it, you will need to add the `sys.path.insert` command to the configuration file to tell Sphinx where to look for Bacch.

```python
import sys
sys.path.insert(0,'/path/to/bacch')
extensions = ['bacch']
```



### Initializing a Project

For the moment, there is no initialization script available to automate setting up new projects to use Bacch.  You need to manually create the relevant directories and the configuration file.

There are two directories in a project:

- The source directory, which contains the source files of your book and the configuration file.

- The build directory, to which Sphinx writes the output.

For the sake of convenience, these directories are referred to as `source/` and `build/`, but it does not matter what names you give them.  The `sphinx-build` command identifies them through positional arguments.

#### Configuration File

In addition to creating the directories, you also need to write the configuration file yourself.  By default, Sphinx looks in the source directory for a file named `conf.py`.

The configuration file is a Python program in its own right and requires consistent syntax for the assigned variables.  There are some options that you must set for Sphinx and some options that you must set for Bacch

```python
import sys
sys.path.insert(0, '/path/to/bacch')
extensions = ['bacch']

master_doc = 'index'
source_suffix = '.rst'
```

The first three lines are about making the Bacch extension available, the last two define where the build should start. 

Using the `sys` module, it adds the path to the Bacch repository on your system to Python.  Now when Sphinx parses the `extensions` list, it is able to find the Bacch extension.

Sphinx uses `master_doc` to identify the file it should use to start the build.  By convention, this file is called `index.rst` given that Sphinx is often used to build documentation websites.  You can use any name you like, provided you define it here.  The `source_suffix` parameter defines the type of files that Sphinx should read.


### Configuration

When you initialize the project, you need to create a configuration file in the source directory, called `conf.py`.  In addition to the basic settings to show Sphinx where to look for the Bacch extension, there are a number of project and formatting parameters available to help in fine tuning the PDF.

#### Project Variables

##### `bacch_buildtype`

Defines the build type that Sphinx should run by default.

Currently, Bacch only supports trade paperback as an output format.  Standard manuscript format and chapter builds are to be implemented at a later date.


| Parameter         | Type  | Default |
|-------------------|-------|---------|
| `bacch_buildtype` | `str` | `'TPB'` |


##### `bacch_show_todo`

Defines whether you want todo blocks to appear in the output.

Currently, Bacch does not support todo blocks and Sphinx reads them as comments, rendering no output.  In the future, when this parameter is set to `True`, Bacch will output a special admonition block for todos.


| Parameter         | Type  | Default |
|-------------------|-------|---------|
| `bacch_show_todo` | `bool`| `False` |


#### Metadata Variables


##### `bacch_author`

Defines the author of the book.

Bacch uses this parameter to define the LaTeX variable for the title page.  Currently, it only supports formatting for books with a single author.


| Parameter      | Type  | Default     |
|----------------|-------|-------------|
| `bacch_author` | `str` | `Anonymous` |


##### `bacch_pubcities`

Defines the cities in which the publisher is based.

Bacch uses this variable on the title page to show the cities in which the publisher is based.  The list is parsed during build and arranged with separators under the publisher.

| Parameter         | Type  | Default |
|-------------------|-------|---------|
| `bacch_pubcities` | `list` | `[]`   |


##### `bacch_publisher`

Defines the publisher of the book.

Bacch uses this variable on the title page to show the book's publisher.

| Parameter         | Type  | Default |
|-------------------|-------|---------|
| `bacch_publisher` | `str` | ``      |


##### `bacch_surname`

Defines the surname of the book's author.

Bacch uses this parameter to define the LaTeX variable for the author name that appears in the runner at the top of the page.  This variable only gets used when you set `bacch_header_type` or `bacch_footer_type` to a format that include the surname.


| Parameter       | Type  | Default      |
|-----------------|-------|--------------|
| `bacch_surname` | `str` | `'Anonymous'`|


##### `bacch_title`

Defines the title of the book.

Bacch uses this variable on the title page of the book.

| Parameter       | Type  | Default     |
|-----------------|-------|-------------|
| `bacch_title`   | `str` | `'Untitled'`|


##### `bacch_title_runner`

Defines the runner title of the book.

When you define formats for `bacch_header_type` or `bacch_footer_type` that calls for the title, Bacch uses this parameter to define the title that it should use.  This ensures that a short title always appears in the header, which prevents a long title from overrunning the header.


| Parameter             | Type  | Default     |
|-----------------------|-------|-------------|
| `bacch_title_runner`  | `str` | `'Untitled'`|


##### `bacch_title_second`

Defines the second line of the title of the book.

Bacch uses this variable on the title page of the book.  This allows you to extend the main title onto a second line.

For example, in the event that you want to reprint *Frankenstein* through Bacch, you would use `bacch_title_second` for the second line of the title *The Modern Prometheus*.

| Parameter            | Type  | Default |
|----------------------|-------|---------|
| `bacch_title_second` | `str` | `''`    |


##### `bacch_title_subtitle`

Defines the subtitle of the book.

Bacch uses this on the title page.  It renders in italics towards the bottom of the page.  Common usage is to define the type of book that you're writing.  For example, *A Novel* or *A Collection*.


| Parameter             | Type  | Default |
|-----------------------|-------|---------|
| `bacch_title_subtitle`| `str` | `''`    |


#### Typesetting Variables

##### `bacch_chapblock_separator`

Defines the separator for use in the chapter block.

When you define a variable for `bacch_chapter_block` that calls for Bacch to render a block of section and subsection titles, this variable defines the separator that Bacch uses between each entry.


| Parameter                   | Type  | Default |
|-----------------------------|-------|---------|
| `bacch_chapblock_separator` | `str` | `'--'`  |


##### `bacch_chapter_block`

Defines the type of header block to use for each chapter.

>**Note**: This feature is under development and subject to change.

In nonfiction, chapters break down into sections and subsections that have visible titles.  This is not generally the case in fiction, where the breaks occur at the same interval but the titles do not.  By default, Bacch suppresses the visibility of titles for anything smaller than a chapter.

When Sphinx runs, Bacch logs the available titles in a `dict` object.  It can then implement this data in a block at the top of the chapter.  The available options are:

- `'block`': Titles are drawn from the chapter, sections and subsections and renders in bold in a separated list at the top of the chapter.

- `'title-block'`: Titles are drawn from the sections and subsections and renders in a bold in a separated list at the top of the chapter.  Above the block, Bacch renders the chapter title.

- `'titleonly'`: Bacch ignores titles from sections and subsections and instead renders only the chapter title.


| Parameter             | Type  | Default |
|-----------------------|-------|---------|
| `bacch_chapter_block` | `str` | `None`  |


## Release Notes

### Version 0.x

Initial development releases.

**Version 0.4**: After some deliberation chose to transition the project from a standalone application to a Sphinx module.  Stripped out the `bacch.py` wrapper, created a new version of `bacchbuilder.py` and `bacchwriter.py` for the Sphinx components, with new `bacch.py` now relegated to the initializing the builder.  For the moment, plans for XML support abandoned.

**Version 0.3**: First version to successfully run build system top to bottom on a project written in reStructuredText.  Provides configuration options for minor adjustments in formatting.

**Version 0.2**: Developed the `bacchbuilder` Sphinx extension.  When Sphinx is called by itself, able to create a properly formatted PDF document of a novel for trade paperback release. 

**Version 0.1**: First prototype `bacch` system.  `bacch` able to successfully parse XML source code to produce a single HTML document.

