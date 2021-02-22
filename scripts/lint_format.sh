#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

poetry run flake8 src/ --extend-exclude=dist,build --show-source --statistics --max-line-length 120
poetry run black .
poetry run isort --color -n src/
