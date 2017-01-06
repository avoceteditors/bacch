

SETUP = setup.py install --user
PY3 = python3.5 $(SETUP) 
PY2 = python2 $(SETUP)
CALL = bacch


all: install-py3 call

install-py3:
	@$(PY3)
	
install-py2:
	@$(PY2)

testbacch:
	@bacch -Svk test -b html
