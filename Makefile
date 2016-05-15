PYTHON = python3
INSTALL = install
DEVELOP = develop
TARGET = setup.py
TRASH = build/ dist/ *.egg-info

all: install

install:
	@echo "============="
	@echo "|  INSTALL  |"
	@echo "============="
	$(PYTHON) $(TARGET) $(INSTALL)

develop:
	@echo "============="
	@echo "|  DEVELOP  |"
	@echo "============="
	$(PYTHON) $(TARGET) $(DEVELOP)

clean:
	@echo "============="
	@echo "|CLEAN BUILD|"
	@echo "============="
	rm -rf -v $(TRASH)