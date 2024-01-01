#!/usr/bin/env bash
# exit on error
set -o errexit

python manage.py loaddata category
python manage.py loaddata subcategory
python manage.py loaddata course