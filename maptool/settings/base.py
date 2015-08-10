"""
Django settings for maptool project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import abspath, basename, dirname, join, normpath
from django.core.urlresolvers import reverse_lazy
from sys import path
from .secure import SECURE_SETTINGS
BASE_DIR = dirname(dirname(__file__))


# Absolute filesystem path to the Django project config directory:
# (this is the parent of the directory where this file resides,
# since this file is now inside a 'settings' pacakge directory)
DJANGO_PROJECT_CONFIG = dirname(dirname(abspath(__file__)))
#print '%s' % DJANGO_PROJECT_CONFIG
# Absolute filesystem path to the top-level project folder:
# (this is one directory up from the project config directory)
SITE_ROOT = dirname(DJANGO_PROJECT_CONFIG)
#print '%s' % SITE_ROOT
# Site name:
SITE_NAME = basename(SITE_ROOT)
#print '%s' % SITE_NAME
# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(SITE_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECURE_SETTINGS.get('django_secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'djangular',
    'django_auth_lti',
    'basic_lti_app',
    'maptoolapp',
    'maps',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cached_auth.Middleware',
    'django_auth_lti.middleware.LTIAuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
AUTHENTICATION_BACKENDS = (
    'django_auth_lti.backends.LTIAuthBackend',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'


LOGIN_URL = reverse_lazy('lti_auth_error')

ROOT_URLCONF = 'maptool.urls'

WSGI_APPLICATION = 'maptool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/lti_tools/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    normpath(join(SITE_ROOT, 'static')),
)

STATIC_ROOT = normpath(join(SITE_ROOT, 'http_static'))

# List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
#     #'django.template.loaders.eggs.Loader',
# )
#
# TEMPLATE_DIRS = (
#     normpath(join(SITE_ROOT, 'templates')),
# )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LTI_OAUTH_CREDENTIALS = SECURE_SETTINGS.get('lti_oauth_credentials', None)


# Tool specific settings
MAP_TOOL_APP = {
    'google_map_api_v3_key': SECURE_SETTINGS.get('google_map_api_v3_key'),
    'required_lti_params' : [
        'resource_link_id',
        'user_id',
        ]
}

# Tool specific settings
MAPS = {
    'google_map_api_v3_key': SECURE_SETTINGS.get('google_map_api_v3_key'),
    'required_lti_params' : [
        'resource_link_id',
        'user_id',
        ]
}

FIXTURE_DIRS = (
    '/maptoolapp/fixtures/',
)
# CRISPY_FAIL_SILENTLY = not DEBUG