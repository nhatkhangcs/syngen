# Command
VENV_DIR_NAME = .venv
CWD = $(shell pwd)

PYTHON = python
ifeq ($(PYTHON),)
  $(error "Python is not installed on this system!")
endif

PIP = pip
ifeq ($(PIP),)
  $(error "Pip is not installed on this system!")
endif

ifeq ($(OS), Windows_NT)
	UNAME_S = Windows_NT
else
	UNAME_S = $(shell uname -s)
endif

# Color
RED    := \033[1;91m
GREEN  := \033[1;92m
YELLOW := \033[1;93m
CYAN   := \033[1;96m
RESET  := \033[0m

ifeq ($(UNAME_S), Windows_NT)
	# For Windows, using Python to print colored text
	PRINT_CYAN 		= $(PYTHON) -c 'print("\033[1;96m" + "$(1)" + "\033[0m")'
	PRINT_GREEN 	= $(PYTHON) -c 'print("\033[1;92m" + "$(1)" + "\033[0m")'
	PRINT_YELLOW 	= $(PYTHON) -c 'print("\033[1;93m" + "$(1)" + "\033[0m")'
	PRINT_RED 		= $(PYTHON) -c 'print("\033[1;91m" + "$(1)" + "\033[0m")'
else
	# For Unix-based systems, using echo to print colored text
	PRINT_CYAN 		= @echo "$(CYAN)$(1)$(RESET)"
	PRINT_GREEN		= @echo "$(GREEN)$(1)$(RESET)"
	PRINT_YELLOW	= @echo "$(YELLOW)$(1)$(RESET)"
	PRINT_RED 		= @echo "$(RED)$(1)$(RESET)"
endif

define cyan
	$(call PRINT_CYAN,$(1))
endef

define green
	$(call PRINT_GREEN,$(1))
endef

define yellow
	$(call PRINT_YELLOW,$(1))
endef

define red
	$(call PRINT_RED,$(1))
endef


ifeq ($(UNAME_S), Linux)
	ACTIVATE = source $(VENV_DIR_NAME)/bin/activate
else ifeq ($(UNAME_S), Darwin)
	ACTIVATE = source $(VENV_DIR_NAME)/bin/activate  # macOS
else  # Assume Windows
	ACTIVATE = .\\$(VENV_DIR_NAME)\\Scripts\\activate
endif

PY_VERSION := $(shell $(ACTIVATE) && $(PYTHON) --version)

.PHONY: help test package clean install venv check_env

help:	### The following lines will print the available commands when entering just 'make'
ifeq ($(UNAME_S), Linux)
	@grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
else ifeq ($(UNAME_S), Windows_NT) # For Window
	$(call cyan, "check_os   : Check the OS and venv settings")
	$(call cyan, "clean      : Clean up files")
	$(call cyan, "install    : Install dependencies")
	$(call cyan, "install_dev: Install developer dependencies")
	$(call cyan, "package    : Create package")
	$(call cyan, "test       : Run tests")
else # For MaxOS
	@awk -F ':.*###' '$$0 ~ FS {printf "\033[36m%15s\033[0m%s\n", $$1 ":", $$2}' \
		$(MAKEFILE_LIST) | grep -v '@awk' | sort
endif

check_env:	### Checking environment, e.g. script creating venv && operating system && ...
	@printf "CWD    : "
	$(call green, "$(CWD)")
	@printf "MAKE   : "
	$(call green,"$(MAKEFILE_LIST)")
	@printf "OS     : "
	$(call green, "$(UNAME_S)")
	@printf "VENV   : "
	$(call green, "$(ACTIVATE)")
	@printf "PY_VER : "
	$(call green, "$(PY_VERSION)")

test: ### Runs all the project tests
	$(call green, "Run tests")
	$(ACTIVATE) && $(PIP) install pytest && $(PYTHON) -m pytest tests/

package: ### Runs the project setup
	@echo "$(version)" > VERSION
	$(ACTIVATE) && $(PYTHON) -m build --wheel
	$(ACTIVATE) && $(PYTHON) -m twine check dist/*

clean: ### Removes build binaries file and distribute file
	$(call red, "Removing build and dist directories")
	rm -rf build dist

install_dev: install ### Installs required dependencies for developers
	$(call green, "Installing requirements for developers")
	$(ACTIVATE) && $(PIP) install -r requirements/requirements-dev.txt
	$(ACTIVATE) && $(PIP) install -e ".[dev,test]"

install: ### Installs required dependencies for users
	$(call green, "Installing requirements for users")
	$(ACTIVATE) && $(PIP) install -r requirements/requirements.txt
	$(ACTIVATE) && $(PIP) install -e .
