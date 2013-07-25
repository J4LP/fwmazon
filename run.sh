#!/bin/sh
./manage.py syncdb
./manage.py migrate account
./manage.py migrate eve
./manage.py migrate shop
./manage.py migrate checkout
gunicorn fwmazon.wsgi