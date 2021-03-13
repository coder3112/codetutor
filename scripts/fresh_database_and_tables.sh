#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

function is_database() {
  psql -lqt | cut -d \| -f 1 | grep -wq $1
}

drop_db='DROP DATABASE IF EXISTS codetutor;'
create_db='CREATE DATABASE codetutor;'
run_migrations='python run_migrations.py'

if is_database 'codetutor'
then
  psql -c $drop_db
else
  echo codetutor does not exist
fi

psql -c $create_db
bash -c $run_migrations
