# Bacch

Writers that work on large projects such as books or documentation, often encounter various technical limitations in word processors.  While a word processor can prove effective in smaller works, such as letters and resumes, as the project grows they become progressively more difficult to work in.  Consistent chapter and section counts, management of typesetting and project statistics increase exponentially with the scale of the project.

Documentation writers have had a handle on these issues for decades.  Instead of trying to do everything from one large application, the job is broken up into a number of smaller programs.  You write your docs in a text editor using a markup language of some kind to show how each file fits with the project and then you run a program on the source directory, processing the files to produce a website or a PDF.  The Python Project developed Sphinx in order to meet this latter functionality.

Writers working with Sphinx produce documentation in the reStructuredText markup language.  Sphinx then processes the documentation to produce versions in HTML, ePub, manpages, JSON, LaTeX/PDF, and so on.

While Sphinx is a very effective tool for documentation, the threshold of technical knowledge is rather high for writers working in other fields.  Additionally, the default implementation of the LaTeX/PDF builder does not work very well for writers working in other genres.

Bacch is a Sphinx extension with the specific goal of providing writers from nontechnical backgrounds with the more advanced tools standard for those working in documentation.  Development targets ease of use and print output.




## Documentation

Revised documentation is in development at [Avocet Editorial Consultants](http://avoceteditors.com).




### Initializing a Project

Currently, there is no script ready to initialize a project.  Follow the standard conventions for Sphinx, or the `sphinx-quickstart` script.

>Bear in mind that `sphinx-quickstart` was developed for setting up documentation projects, not books.  The way it configures `conf.py` is not especially useful to writers working outside of this field and genre.  

Python does not know where you installed Bacch by default.  When Sphinx runs, if it can't find the builder it aborts the operation.  To show it where to look, add the path to Bacch in the `conf.py` configuration file.

```python
import sys
sys.path.insert(0,'/path/to/bacch/')
```

### Using Bacch

Currently, Bacch does not feature a wrapper script to simplify running Sphinx.  You need to run it manually from the project directory.  Bacch provides two builders for processing your book:

- **bacch** The default builder compiles the entire project into a single LaTeX file formatted for trade paperback.
- **gnomon** The review builder compiles each individual file in the source directory into LaTeX formatted to print for editing and review.

Bear in mind, Bacch currently only processes the document into LaTeX and requires an external LaTeX processor, such as `rubber` or `pdflatex` to take the last step in creating a PDF.

To build the LaTeX for the entire project, run:

```sh
$ sphinx-build -b bacch sourcedir outputdir
```

To build the LaTeX for individual chapters, run:

```sh
$ sphinx-build -b gnomon sourcedir outputdir
```




## Contribution

If you notice a bug, would like to make a suggestion or have a feature request: create an issue on this repository.


## Version History

### Version 0.x

Initial Development Releases:

**Version 0.5**: Reorganization of the repo for better management of code.  Introduces the gnomon builder as a companion to the bacch builder.  Where the bacch builder processes the entire project into LaTeX for a PDF in trade paperback format, gnomon processes single chapters to print at home for review.

**Version 0.4**: Project transitions to straight reST through Sphinx.  XML support abandoned, given the contention that users that write in XML have sufficient skill as to use XSLT on their own, without Bacch.

**Version 0.3**: Bacch able to run proper builds without error.  Introduces configuration options for minor adjustments in formatting.

**Version 0.2**: First Sphinx extension.  Bacch able to create a LaTeX document through Sphinx.  `pdflatex` then called to convert this into a PDF in trade paperback format.

**Version 0.1**: First prototype: Bacch able to successfully parse XML source code to produce a single HTML document.


