

SETUP = setup.py install --user
PY3 = python3.5 $(SETUP) 
PY2 = python2 $(SETUP)
CALL = bacch



install-py3:
	@$(PY3)
	
install-py2:
	@$(PY2)

call:
	@echo ""
	@echo ""
	@bacch -v
