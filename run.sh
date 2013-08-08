#!/bin/sh
redis-server /etc/redis/redis.conf
python manage.py syncdb
python manage.py migrate account
python manage.py migrate eve
python manage.py migrate shop
python manage.py migrate checkout
.heroku/python/bin/python manage.py run_huey &> huey_console.log &
gunicorn fwmazon.wsgi --log-syslog --log-level warning
