# -*- coding: utf-8 -*-

import os
from django.core.urlresolvers import reverse_lazy
#import djcelery
import dj_database_url

# djcelery.setup_loader()
# BROKER_URL = 'amqp://guest:guest@localhost:5672/'
# CELERY_RESULT_BACKEND = "amqp"

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

DEBUG = os.getenv('FW_DEBUG', False)

# Databases that we read from the environment
if DEBUG:
    DATABASES = {
        'default' : {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_PATH, 'db.sqlite3')
        }
    }
else:
    DATABASES = {}
    DATABASES['default'] =  dj_database_url.config()

ALLOWED_HOSTS = ['*']

# Fwehman Brothers Holdings
FW_KEY_ID = 2338850
FW_VCODE = 'Fr0T2PitfHnyjIkHXERzwbqMGBGh82ZfQiPLCOebRAgSRm10zdIxNzavM1YAQ8Lm'
FW_WALLET = 1000

AUTH_USER_MODEL = 'account.User'

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Vadrin Hegirin', 'vadrin@fweddit.com')
)

LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')

MANAGERS = ADMINS

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = os.path.join(PROJECT_PATH, '../', 'static_files')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, '../', 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g=ma54%c!fayddzz1jy8l!ww#89cuwyub*bb6r*prte(%a*-^5'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'shop.middleware.CartMiddleware',
)

ROOT_URLCONF = 'fwmazon.urls'

WSGI_APPLICATION = 'fwmazon.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH   , '../', 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'shop.context_processors.cart',

)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'south',
    'djcelery',
    'mathfilters',
    'home',
    'eve',
    'manager',
    'shop',
    'checkout',
    'account',
)

if not os.path.exists(os.path.join(PROJECT_PATH   , '../', 'logs')):
    os.makedirs(os.path.join(PROJECT_PATH   , '../', 'logs'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'stash_format': {
            '()': 'logstash_formatter.LogstashFormatter'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'backupCount': 50,
            'maxBytes': 2 ** 20,
            'filename': 'logs/fwmazon.log'
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.LogstashHandler',
            'host': '172.16.42.1',
            'port': 5234
        }
    },
    'loggers': {
        'fwmazon': {
            'handlers': ['syslog', 'console', 'logstash'],
            'level': 'INFO',
        }
    }
}