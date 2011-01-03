# Django settings for src project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'opentrackings',
        'USER':     'otadmin',
        'PASSWORD': '',
        'HOST':     '',
        'PORT':     '',
        'OPTIONS': {"init_command": "SET storage_engine=INNODB"},
    }
}

import os

SITE_ROOT = os.path.realpath(os.path.abspath(os.path.join(os.path.realpath(os.path.dirname(__file__)), '..')))
MEDIA_ROOT = os.path.realpath(os.path.abspath(os.path.join(SITE_ROOT, 'media')))

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

SITE_URL = ''
MEDIA_URL = '%smedia/' % SITE_URL

# Absolute path to the directory that holds media.
MEDIA_ROOT = '/www/opentrackings/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
MEDIA_URL = 'http://opentrackings.com/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
ADMIN_MEDIA_PREFIX = '/django-admin-media/'

LOGIN_URL = 'account/signin/'
LOGIN_REDIRECT_URL = "/"
ACCOUNT_ACTIVATION_DAYS = 10

OPENID_SREG = {
    "required": ['fullname', 'country']
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ABCDEFGHIJKLMNOPQRST1234567890'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django_authopenid.context_processors.authopenid',
)

ROOT_URLCONF = 'opentrackings.urls'

TEMPLATE_DIRS = (
     os.path.realpath(os.path.abspath(os.path.join(SITE_ROOT, 'opentrackings', 'templates'))),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'opentrackings.apps.opentrackings',
    'uni_form',
    'registration',
    'django_authopenid',
)
