"""
Django settings for chores project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join, normpath
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+-qo9*o7c4z42t+x8z7370199j@q-*osb5)p*!01t7jyg&pvbw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMINS = (
    ('William Collins', 'wcurtiscollins@gmail.com'),
)

SERVER_EMAIL = 'django@getmize.com'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    join(BASE_DIR,  'chores/templates'),
)

STATIC_ROOT = normpath(BASE_DIR)
STATIC_URL = '/static'
STATICFILES_DIRS = (
    normpath(join(BASE_DIR, 'assets')),
    normpath(join(BASE_DIR, 'bower_components')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

PIPELINE_ENABLED = False

PIPELINE_JS = {
    'app': {
        'source_filenames': (
            'jquery/dist/jquery.js',
            'jquery-ui/jquery-ui.min.js',
            'jquery-ui/ui/datepicker.js',
            'mustache/mustache.js',
            'moment/moment.js',
            'modernizr/modernizr.js',
            'underscore/underscore.js',
            'js/app.coffee',
            'js/facebook.js',
            'js/jstz.js',
        ),
        'output_filename': 'js/app.js',
    },
    'chores': {
        'source_filenames': (
            'angular/angular.js',
            'angular-route/angular-route.js',
            'angular-resource/angular-resource.js',
            'foundation/js/foundation.js',
            'foundation/js/foundation/foundation.reveal.js',
            'js/chores/app.coffee',
            'js/chores/base_services.coffee',
            'js/chores/services.coffee',
            'js/chores/controllers.coffee',
            'js/chores/directives.coffee',
        ),
        'output_filename': 'js/chores.js',
    }
}

PIPELINE_CSS = {
    'app': {
        'source_filenames': (
            'foundation/css/foundation.css',
            'font-awesome/css/font-awesome.css',
            'css/dates.sass',
            'css/app.sass',
        ),
        'output_filename': 'js/app.css',
    }
}

PIPELINE_COMPILERS = (
   'pipeline.compilers.sass.SASSCompiler',
   'pipeline.compilers.coffee.CoffeeScriptCompiler'
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'south',
    'djcelery',
    'pipeline',
    'coverage',
    'chores'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chores.middleware.UserMiddleware',
    'chores.middleware.JSONMiddleware',
)

ROOT_URLCONF = 'chores.urls'

WSGI_APPLICATION = 'chores.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chores',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379:1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# CELERY SETTINGS
BROKER_URL = 'redis://127.0.0.1:6379:1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

SECRET = 'captain hook polymorph my eggshells'

SESSION_ENGINE = 'redis_sessions.session'

# Facebook test site credentials
APP_ID = '332305020261516'
APP_SECRET = '3a54fc53a73878ed337e768eb0d2e1c7'

# Twilio credentials
TWILIO_ACCOUNT_SID = 'ACb388d04293abdbe17968b51fa16c74f2'
TWILIO_AUTH_TOKEN = '121fa6726edce5d4c104bbf4697ce330'
TWILIO_NUM = '+18194142120'

GENERIC_USER_PASSWORD = 'HSOUH12849&^$(asdf'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTHENTICATION_BACKENDS = (
    'chores.backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

try:
    from .local import *
except ImportError:
    pass

import sys
if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    DATABASES['default']['engine'] = 'sqlite3'
