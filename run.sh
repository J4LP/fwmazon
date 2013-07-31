#!/bin/sh
python manage.py syncdb
python manage.py migrate account
python manage.py migrate eve
python manage.py migrate shop
python manage.py migrate checkout
.heroku/python/bin/python manage.py celery worker -B --broker=amqp://guest@172.16.42.1:5672/ --loglevel=DEBUG &> celery.log &
gunicorn fwmazon.wsgi --log-syslog --log-level warning
