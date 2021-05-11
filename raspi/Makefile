FILEPATH :=

# Lint.  Uses flake8
.PHONY: lint
lint: 
	@echo "Linting with flake8"
	@flake8 $(FILEPATH)

.PHONY: format
format:
	@echo "Formatting with autopep8"
	@autopep8 --in-place --recursive .