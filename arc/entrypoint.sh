#!/bin/bash

# wait for Postgres to start
sleep 15
# python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"
