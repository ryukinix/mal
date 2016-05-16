PYTHON = python3
INSTALL = install
DEVELOP = develop
TARGET = setup.py
TEST_DEPLOY = sdist upload --repository pypitest
REGISTER = register --repository pypitest
DEPLOY = sdist upload --repository pypi
REGISTER = register --repository pypi
TRASH = build/ dist/ *.egg-info
CHECK = check --metadata --restructuredtext --strict

all: install
	 clean

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
	@echo "+===============+"
	@echo "| TEST-REGISTER |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(REGISTER) 

test-deploy:
	@echo "+===============+"
	@echo "| TEST-DEPLOY   |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(TEST_DEPLOY) 

deploy:
	@echo "+===============+"
	@echo "|   DEPLOY      |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(DEPLOY)

check:
	@echo "+===============+"
	@echo "|     CHECK     |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(CHECK)
	@echo "ok!"

register:
	@echo "+===============+"
	@echo "|   REGISTER    |"
	@echo "+===============+"
	$(PYTHON) $(TARGET) $(REGISTER)

clean:
	@echo "+===============+"
	@echo "|  CLEAN BUILD  |"
	@echo "+===============+"
	rm -rf -v $(TRASH)