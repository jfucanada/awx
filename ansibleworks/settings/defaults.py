# Copyright (c) 2013 AnsibleWorks, Inc.
# All Rights Reserved.

import os
import sys

# Update this module's local settings from the global settings module.
from django.conf import global_settings
this_module = sys.modules[__name__]
for setting in dir(global_settings):
    if setting == setting.upper():
        setattr(this_module, setting, getattr(global_settings, setting))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

REST_FRAMEWORK = {
    'FILTER_BACKEND': 'ansibleworks.main.custom_filters.CustomFilterBackend',
    'DEFAULT_PAGINATION_SERIALIZER_CLASS': 'ansibleworks.main.serializers.PaginationSerializer',
    'PAGINATE_BY': 25,
    'PAGINATE_BY_PARAM': 'page_size',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'acom.sqlite3'),
        # Test database cannot be :memory: for celery/inventory tests to work.
        'TEST_NAME': os.path.join(BASE_DIR, 'acom_test.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
#
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

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Absolute filesystem path to the directory where static file are collected via
# the collectstatic command.
STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/static/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media') # FIXME: Is this where we want it?

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute filesystem path to the directory to host projects (with playbooks).
# This directory should not be web-accessible.
PROJECTS_ROOT = os.path.join(BASE_DIR, 'projects')

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'p7z7g1ql4%6+(6nlebb6hdk7sd^&fnjpal308%n%+p^_e6vo1y'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'ansibleworks.ui.context_processors.settings',
)

MIDDLEWARE_CLASSES += (
    'ansibleworks.middleware.exceptions.ExceptionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    # middleware loaded after this point will be subject to transactions
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

ROOT_URLCONF = 'ansibleworks.urls'

WSGI_APPLICATION = 'ansibleworks.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'south',
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'djcelery',
    'kombu.transport.django',
    'taggit',
    'ansibleworks.main',
    'ansibleworks.ui',
)

INTERNAL_IPS = ('127.0.0.1',)

# Email address that error messages come from.
SERVER_EMAIL = 'root@localhost'

# Default email address to use for various automated correspondence from
# the site managers.
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

# Subject-line prefix for email messages send with django.core.mail.mail_admins
# or ...mail_managers.  Make sure to include the trailing space.
EMAIL_SUBJECT_PREFIX = '[AnsibleWorks] '

# The email backend to use. For possible shortcuts see django.core.mail.
# The default is to use the SMTP backend.
# Third-party backends can be specified by providing a Python path
# to a module that defines an EmailBackend class.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending email.
EMAIL_HOST = 'localhost'

# Port for sending email.
EMAIL_PORT = 25

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

# Use Django-Debug-Toolbar if installed.
try:
    import debug_toolbar
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
except ImportError:
    pass

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'ENABLE_STACKTRACES' : True,
}

# Use Django-devserver if installed.
try:
    import devserver
    INSTALLED_APPS += ('devserver',)
except ImportError:
    pass

DEVSERVER_DEFAULT_ADDR = '0.0.0.0'
DEVSERVER_DEFAULT_PORT = '8013'
DEVSERVER_MODULES = (
    'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',
    #'devserver.modules.ajax.AjaxDumpModule',
    #'devserver.modules.profile.MemoryUseModule',
    #'devserver.modules.cache.CacheSummaryModule',
    #'devserver.modules.profile.LineProfilerModule',
)

# Skip migrations when running tests.
SOUTH_TESTS_MIGRATE = False

if 'djcelery' in INSTALLED_APPS:
    import djcelery
    djcelery.setup_loader()

BROKER_URL = 'django://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TRACK_STARTED = True
CELERYD_TASK_TIME_LIMIT = 3600
CELERYD_TASK_SOFT_TIME_LIMIT = 3540
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_MAX_LOOP_INTERVAL = 60

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)-8s %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'null': {
            'class': 'django.utils.log.NullHandler',
        },
        'file': {
            'class': 'django.utils.log.NullHandler',
            'formatter': 'simple',
        },
        'syslog': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.NullHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins', 'console', 'file', 'syslog'],
            'level': 'WARNING',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'ansibleworks': {
            'handlers': ['console', 'file', 'syslog'],
            'level': 'DEBUG',
        },
        'ansibleworks.main.rbac': {
            'handlers': ['null'],
            # Comment the line below to show lots of permissions logging.
            'propagate': False,
        },
        'ansibleworks.main.access': {
            'handlers': ['null'],
            # Comment the line below to show lots of permissions logging.
            'propagate': False,
        },
    }
}
