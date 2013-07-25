#!/bin/sh
python manage.py syncdb
python manage.py migrate account
python manage.py migrate eve
python manage.py migrate shop
python manage.py migrate checkout
gunicorn fwmazon.wsgi