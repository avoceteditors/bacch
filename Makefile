

SETUP = setup.py install --user
PY3 = python3 $(SETUP) 
CALL = bacch
SRC = test/source
OUT = test/build


install:
	@$(PY3)

all: install call

call:
	@echo ""
	@echo ""
	@sphinx-build -b bacch $(SRC) $(OUT)
