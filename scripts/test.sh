#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

if [[ -z "${TRAVIS}"]]; then
  bash scripts/fresh_database_and_tables.sh
fi
python create_admin_user.py
python -m pytest -s
