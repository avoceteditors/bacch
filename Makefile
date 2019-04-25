

SETUP = setup.py install --user
PY3 = python3 $(SETUP) 
CALL = bacch
SRC = test/source
OUT = test/build


install:
	@$(PY3)

all: install call

call:

call-all:
	@sphinx-build -avTb bacch $(SRC) $(OUT)

call-some:
	@sphinx-build -vnb bacch $(SRC) $(OUT)
