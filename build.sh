#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Diagnostic: List files to see if they exist
ls -R static

# BRUTE FORCE: Manually copy files because Django's collectstatic is failing
mkdir -p staticfiles
cp -r static/* staticfiles/

python manage.py collectstatic --no-input
python manage.py migrate

# Final Verification
ls -R staticfiles
