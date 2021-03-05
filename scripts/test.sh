#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

python create_admin_user.py
python -m pytest -s
