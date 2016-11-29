

SETUP = setup.py install --user
PY3 = python3 $(SETUP) 
PY2 = python2 $(SETUP)
CALL = bacch

SRC = test/test-source
OUT = test/test-output

all: install-py3 call

install-py3:
	@$(PY3)
	
install-py2:
	@$(PY2)

call:
	@bacch -Svk test 
