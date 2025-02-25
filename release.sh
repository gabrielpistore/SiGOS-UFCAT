#!/bin/bash

# Exit on any error
set -e

python manage.py migrate
python manage.py seed
