PYTHON = python3
INSTALL = install
DEVELOP = develop
TARGET = setup.py
TEST_DEPLOY = sdist upload --repository pypitest
TEST_REGISTER = register --repository pypitest
DEPLOY = sdist upload --repository pypi
REGISTER = register --repository pypi
TRASH = build/ dist/ *.egg-info
CHECK = check --metadata --restructuredtext --strict
CLEAN = clean
UNINSTALL = --uninstall

all: install
	 clean

check:
	@echo "+===============+"
	@echo "|     CHECK     |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(CHECK)
	@echo "ok!"

install:
	@echo "+===============+"
	@echo "|    INSTALL    |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(INSTALL)

develop:
	@echo "+===============+"
	@echo "|    DEVELOP    |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(DEVELOP)

test-register:
	@make check
	@echo "+===============+"
	@echo "| TEST-REGISTER |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(TEST_REGISTER) 

test-deploy:
	@make check
	@echo "+===============+"
	@echo "| TEST-DEPLOY   |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(TEST_DEPLOY) 

deploy:
	@make check
	@echo "+===============+"
	@echo "|   DEPLOY      |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(DEPLOY)


register:
	@make check
	@echo "+===============+"
	@echo "|   REGISTER    |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(REGISTER)

clean:
	@echo "+===============+"
	@echo "|  CLEAN BUILD  |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(CLEAN)
	$(PYTHON) $(TARGET) $(DEVELOP) $(UNINSTALL)
	find . -name __pycache__ | xargs rm -rfv;
	rm -rf -v $(TRASH)