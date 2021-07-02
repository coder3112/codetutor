#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

bash scripts/fresh_database_and_tables.sh
python create_admin_user.py
python -m pytest -s
