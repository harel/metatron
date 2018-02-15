SHELL := /bin/bash
APPLICATION_NAME="Metatron"
APPLICATION_VERSION=0.1

# Colour coding for output
COLOUR_NONE=\033[0m
COLOUR_GREEN=\033[32;01m
COLOUR_YELLOW=\033[33;01m

TEST="metatron.tests"
SCHEMA=""

.PHONY: help test run
help:
		@echo -e "$(COLOUR_GREEN)|--- $(APPLICATION_NAME) [$(APPLICATION_VERSION)] ---|$(COLOUR_NONE)"
		@echo -e "$(COLOUR_YELLOW)make test$(COLOUR_NONE) : Run the test suite"
		@echo -e "$(COLOUR_YELLOW)make run URL=url$(COLOUR_NONE) SCHEMA=og|twitter: Process a single url"


test:
		python -m unittest $(TEST)


run:
		python -m metatron.metatron $(URL) $(SCHEMA)
