

SETUP = setup.py install --user
PY3 = python3 $(SETUP) 
PY2 = python2 $(SETUP)
CALL = bacch

SRC = test/test-source
OUT = test/test-output

TMP = test/output/latex/tmp


all: install-py3 call

install: install-py3

install-py3:
	@$(PY3)
	
install-py2:
	@$(PY2)

call: 
	@bacch -Svk test -b latex

page: install-py3
	@bacch -Svk test -b html

BOOK = book1-test
book: $(TMP)/$(BOOK).pdf

$(TMP)/$(BOOK).pdf: call
	@pdflatex --output-dir=$(TMP) $(TMP)/$(BOOK).tex
