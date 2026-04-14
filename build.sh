#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Diagnostic: List files to see if they exist
ls -R static

python manage.py collectstatic --no-input --clear
python manage.py migrate
