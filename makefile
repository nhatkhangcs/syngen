PYTHON = python3
PIP = pip3
VENV_DIR_NAME = .venv

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S), Linux)
	ACTIVATE = source $(VENV_DIR_NAME)/bin/activate
else ifeq ($(UNAME_S), Darwin)
	ACTIVATE = source $(VENV_DIR_NAME)/bin/activate  # macOS
else  # Assume Windows
	ACTIVATE = .\\$(VENV_DIR_NAME)\\Scripts\\activate
endif

# Color
RED = \033[1;91m
GREEN = \033[1;92m
YELLOW = \033[1;93m
RESET = \033[0m

.PHONY: help test package clean install venv check_os

help:	## The following lines will print the available commands when entering just 'make'
ifeq ($(UNAME_S), Linux)
	@grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
else
	@awk -F ':.*###' '$$0 ~ FS {printf "%15s%s\n", $$1 ":", $$2}' \
		$(MAKEFILE_LIST) | grep -v '@awk' | sort
endif

check_os:	### Checking script creating venv && operating system
	@echo "OS:   $(GREEN)$(UNAME_S)$(RESET)"
	@echo "VENV: $(GREEN)$(ACTIVATE)$(RESET)"

venv:	## Create virtual environment
	@echo "$(GREEN)Creating virtual environment$(RESET)"
	$(PYTHON) -m venv $(VENV_DIR_NAME)

test: venv ### Runs all the project tests
	@echo "$(GREEN)Run tests$(RESET)"
	$(ACTIVATE) && $(PIP) install pytest && $(PYTHON) -m pytest tests/

package: clean ### Runs the project setup
	@echo "$(version)" > VERSION
	$(ACTIVATE) && $(PYTHON) setup.py sdist bdist_wheel

clean: ### Removes build binaries file and distribute file
	@echo "$(RED)Removing build and dist directories $(RESET)"
	rm -rf build dist

install_dev: venv install ### Installs required dependencies for developers
	@echo "$(GREEN)Installing requirements for $(YELLOW)developers $(RESET)"
	$(ACTIVATE) && $(PIP) install -r requirements/requirements-dev.txt

install: venv ### Installs required dependencies for users
	@echo "$(GREEN)Installing requirements for $(YELLOW)users $(RESET)"
	$(ACTIVATE) && $(PIP) install -r requirements/requirements.txt
