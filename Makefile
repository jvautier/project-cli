# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 project_cli/project_cli.py

clean:
	bash ./tasks/clean.sh $(VENV)

test: venv
	bash ./tasks/test.sh

coverage:
	bash ./tasks/coverage.sh

lint:
	bash ./tasks/lint.sh

format:
	bash ./tasks/format.sh 

.PHONY: all venv run clean test coverage lint format