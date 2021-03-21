# Signifies our desired python version
# Makefile macros (or variables) are defined a little bit differently than traditional bash, keep in mind that in the Makefile there's top-level Makefile-only syntax, and everything else is bash script syntax.
PYTHON = python3

# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help setup test run clean

.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To setup the project(for developing) type make setup"
	@echo "To test the project type make test"
	@echo "To run the project type make run"
	@echo "To run the project in prod mode(AppMode=PROD and use gunicorn) type make run-prod"
	@echo "------------------------------------"

setup:
	@echo "Setting Up"
	pip install poetry
	poetry install --no-root
	poetry shell

test:
	@echo "STARTING TESTS"
	@echo "------------------------------------------------------------------------------------------"
	@bash scripts/test.sh
	
dev:
	@echo "Starting..."
	uvicorn --host 0.0.0.0 --port 8000 --workers 4 --debug src.main:app

prod:
	@echo "Starting..."
	@echo "Using gunicorn"
	fastapi_env=production bash ./start.sh

push:
	@bash scripts/lint_format.sh
	@bash commit.sh
	@echo "Pushing to git repo"
	@eval "$(ssh-agent -s)"
	@ssh-add ~/.ssh/github
	@git push
	@echo "Push complete"
