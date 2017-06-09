#####
Bacch
#####

Sphinx is a document and static site generator built in Python.  It is specifically built to support single-sourcing documentation projects, like the Python Docs.  Writers produce text files in reStructuredText, which Sphinx then converts to HTML and other output formats.  In general, this provides writers with a very efficient and low resource alternative to bloated applications like word processors, which tend to grow exponentially cumbersome on larger projects.  This is all well and good for technical writers, but what about novelists and similar bookwriters?

Sphinx includes a LaTeX builder that produces a very fine PDF, but its focus leans heavily towards documentation whitepapers and is not acceptable for use with the more general classification of books.

Bacch is a Sphinx extension that provides an alternative to the default LaTeX builder and writer.  It generates a LaTeX document then uses a template to apply alternative front matter.  Additionally, it can compile the entire project into one book or operate on individual chapters.



