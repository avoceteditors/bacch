#####
Bacch
#####

Bacch is a document and static site generator built in Python.  Writers work in plain text then parse the text to generate HTML or PDF files.  The goal is to provide a complete, low resource alternative to bloated applications like word processors, which tend to grow cumbersome on larger projects.

**NOTICE:** Bacch has gone through several iteratons over the past few years.  This is mostly due to it being the principal developer's first serious project and partly to some disagreement about an approprate format to use for source files.  As of January 2017, Bacch is amid a heavy overhaul and is currently unusable.


Todo List
=========

Major Features
--------------


Minor Features
--------------

- **Statistics Logger:** Develop a system for compiling word counts.  Each sectional element in a book should receive attribution assignments containing this word count.  FInally, develop a build process to generate a JSON file with the relevant data.  Note, this feature is intended to dovetail with other applications down the road.

- **Markdown Support:** The primary source language for Bacch is DocBook XML, extended with various appliciation-specific control objects.  However, XML can sometimes prove distracting in fiction writing.  

  Feature uses Python Markdown or PyPandoc to convert Markdown files to Docbook/Bacch XML then generate lxml elements for the build system.  Needs to be researched further.

