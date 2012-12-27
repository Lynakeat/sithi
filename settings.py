# Django settings for activebuys project.
import sys
import os

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

sys.path.insert(0, rel('lib'))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'admin@activebuys.com'),
)

MANAGERS = ADMINS

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "server@activebuys.com"
EMAIL_HOST_PASSWORD = "startup123"
EMAIL_USE_TLS = True

SERVER_EMAIL = 'no-reply@activebuys.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': rel('database.sqlite')
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = 'http://s3.amazonaws.com/activebuys-media/'
MEDIA_ROOT = rel('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = rel('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    rel('media'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1xrw3xlz4dyu_s$qxdr84a6aen&lr$lai59txex$#&b4v5&1*lf'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS =(
    'django.contrib.auth.context_processors.auth', 
    'django.core.context_processors.debug', 
    'django.core.context_processors.i18n', 
    'django.core.context_processors.media', 
    'django.core.context_processors.static',
    'django.core.context_processors.request',  
    'django.contrib.messages.context_processors.messages',
    'activebuys.context.get_foxycart_shop_name',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'uturn.middleware.UturnMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

AUTHENTICATION_BACKENDS = ('activebuys.apps.accounts.backends.CustomBackend',)

ROOT_URLCONF = 'activebuys.urls'

TEMPLATE_DIRS = (
    rel('sites/activebuys/templates'),
)

INSTALLED_APPS = (
    'tinymce',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'django.contrib.gis',

    'staging',
    'sorl.thumbnail',
    'south',
    'uturn',
    'refinery',
    'easy_maps',

    'activebuys.apps.companies',
    'activebuys.apps.faq',
    'activebuys.apps.contacts',
    'activebuys.apps.business',
    'activebuys.apps.utils',
    'activebuys.apps.deals', # must be listed after: companies, utils
    'activebuys.apps.accounts', # must be listed after: deals, companies
    'activebuys.apps.vouchers', # must be listed after: accounts
    'activebuys.apps.widget', # must be listed after: accounts
    'activebuys.apps.foxycart',
    'activebuys.apps.zipcodes',
    'activebuys.apps.reviews',
    'activebuys.apps.url_utils',
    'activebuys.apps.follow',
    'activebuys.apps.avatar',

    'pagination', 
)


THUMBNAIL_BASEDIR = 'thumbs'

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

#reviews
REVIEWS_IS_MODERATED = False
REVIEWS_SHOW_PREVIEW = False
REVIEWS_IS_EMAIL_REQUIRED = True
REVIEWS_IS_NAME_REQUIRED = True

#S3 config
from S3 import CallingFormat
#AWS_CALLING_FORMAT = CallingFormat.VANITY
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
AWS_ENABLED = True
AWS_STORAGE_BUCKET_NAME = 'activebuys-media'
AWS_ACCESS_KEY_ID = 'AKIAJZ6I2FD5OETRJEAQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_MEDIA_URL = 'http://activebuys-media.s3.amazonaws.com/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
DEFAULT_FROM_EMAIL = 'no-reply@activebuys.com'

#Campaign monitor api key
CMONITOR_API_KEY = '810da2c1b71d6c31d6f8f29fc392c0fd'
CMONITOR_LIST_ID = 'd23b6e5afa6e4d26f9bfd98dd5beea6e'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

try:
    from local_settings import *
except ImportError:
    pass
