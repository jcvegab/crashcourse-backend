#!/usr/bin/env bash
# exit on error
set -o errexit

uv run python manage.py loaddata category
uv run python manage.py loaddata course
