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

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    join(BASE_DIR,  'chores/templates'),
)

STATIC_ROOT = normpath(join(BASE_DIR, 'static'))
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
            'js/app.js',
            'js/facebook.js',
        ),
        'output_filename': 'js/app.js',
    }
}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'pipeline',
    'chores'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

SESSION_ENGINE = 'redis_sessions.session'

APP_ID = '332305020261516'
APP_SECRET = '3a54fc53a73878ed337e768eb0d2e1c7'

GENERIC_USER_PASSWORD = 'HSOUH12849&^$(asdf'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'wcurtiscollins@gmail.com'
EMAIL_HOST_PASSWORD = 'A42583984g'
EMAIL_PORT = 587

SERVER_EMAIL = 'wcurtiscollins@gmail.com'

try:
    from .local import *
except ImportError:
    pass
