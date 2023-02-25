PYTHON = python3
INSTALL = install
DEVELOP = develop
TARGET = setup.py
TESTS = tests/
DEPLOY = sdist bdist_wheel upload --repository pypi --sign
REGISTER = register --repository pypi
BUILD_GARBAGE = build/ dist/
EGG = *.egg-info
CHECK = check --metadata --restructuredtext --strict
CLEAN = clean
UNINSTALL = --uninstall
BUILD = sdist bdist_wheel

all: install
	 @make clean

dev-dependencies:
	pip install -r requirements-dev.txt

check: check-tests check-package

check-package:
	@echo "+===================+"
	@echo "| PACKAGE INTEGRITY |"
	@echo "+===================+"
	$(PYTHON) $(TARGET) $(CHECK)
	@echo "ok!"

check-tests:
	@echo "+===============+"
	@echo "|     TESTS     |"
	@echo "+===============+"
	$(PYTHON) $(TESTS)
	@echo "ok!"

clean:
	@echo "+===============+"
	@echo "|  CLEAN BUILD  |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(CLEAN)
	find . -name __pycache__ -or -name *.pyc| xargs rm -rfv;
	rm -rfv $(BUILD_GARBAGE)

install:
	@echo "+===============+"
	@echo "|    INSTALL    |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(INSTALL)

build:
	@echo "+===============+"
	@echo "|    BUILD      |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(BUILD)

develop:
	@echo "+===============+"
	@echo "|    DEVELOP    |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(DEVELOP)


develop-uninstall:
	@echo "+===============+"
	@echo "| DEV UNINSTALL |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(DEVELOP) $(UNINSTALL)
	@make clean
	rm -rfv $(EGG)

deploy: dev-dependencies check build
	@make check
	@echo "+===============+"
	@echo "|   DEPLOY      |"
	@echo "+===============+"
	twine upload dist/*


register: dev-dependencies
	@make check
	@echo "+===============+"
	@echo "|   REGISTER    |"
	@echo "+===============+"
	twine register

help:
	@echo "+=============================================+"
	@echo "|                H  E  L  P                   |"
	@echo "+=============================================+"
	@echo "----------------------------------------------"
	@echo "make check:"
	@echo "	 check the build pass on PyPI"
	@echo
	@echo "make clean:"
	@echo "	 clean the build (build/ __pyache__, sdist/)"
	@echo
	@echo "make install:"
	@echo "	 install the package in your system"
	@echo
	@echo "make build:"
	@echo "  build the package as egg-file"
	@echo
	@echo "make develop:"
	@echo "	 install in develop mode (symlink)"
	@echo
	@echo "make develop-uninstall:"
	@echo "	 uninstall develop files and clean build"
	@echo
	@echo "deploy:"
	@echo "	 deploy to PyPY"
	@echo
	@echo "register:"
	@echo "	 register to PyPI"
