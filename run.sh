#!/bin/bash
set -e

mkdir -p /data/cache

python manage.py collectstatic --clear --no-input
python manage.py migrate

exec gunicorn conf.wsgi:application --bind 0.0.0.0:80 $@
