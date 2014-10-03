"""
Django settings for cloudscraper_osse project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# add apps to path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# add wpadmin to path
sys.path.insert(0, os.path.join(BASE_DIR, '..'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&478os2g_tt5g!e+wqgs5h8#-u8ydqhkohnc6u&*yxg9cu@rm5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # Django WP Admin must be before django.contrib.admin
    'wpadmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cores',
    #'websites',
    'django_mailbox',
    'rest_framework',
    'constance',
    'constance.backends.database',
    #'dropbox_plugin',
    'locals',
    'remote',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cloudscraper_osse.urls'

WSGI_APPLICATION = 'cloudscraper_osse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
if "runserver" not in sys.argv:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
else:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WPADMIN = {
    'adminpanel': {
        'admin_site': 'cloudscraper_osse.admin.admin',
        'title': 'Cloudscraper admin panel',
        'menu': {
            'left': 'wpadmin.menu.menus.BasicLeftMenu',
        },
        'dashboard': {
            'breadcrumbs': True,
        },
        'custom_style': STATIC_URL + 'wpadmin/css/themes/sunrise.css',
    },
    'staffpanel': {
        'admin_site': 'cloudscraper_osse.admin.staff',
        'title': 'Cloudscraper staff panel',
        'menu': {
            'left': 'cloudscraper_osse.wp.UserLeftMenu',
        },
        'dashboard': {
            'breadcrumbs': False,
        },
        'custom_style': STATIC_URL + 'wpadmin/css/themes/default.css',
    },
    'userpanel': {
        'admin_site': 'cloudscraper_osse.admin.user',
        'title': 'Cloudscraper user panel',
        'menu': {
            'left': 'cloudscraper_osse.wp.UserLeftMenu',
        },
        'dashboard': {
            'breadcrumbs': False,
        },
        'custom_style': STATIC_URL + 'wpadmin/css/themes/ocean.css',
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : '[%(asctime)s] %(levelname)s %(module)s:%(name)s:%(lineno)s: %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'cloudscraper.log',
            'maxBytes': 1048576,
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file', 'console'],
            'propagate': True,
            'level':'INFO',
        },
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    }
}

#MEDIA_ROOT = os.path.join(BASE_DIR, 'apps/django_mailbox/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'apps/cores/incoming/')
MEDIA_URL = "/media/"

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    #'DEFAULT_MODEL_SERIALIZER_CLASS':
        #'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        #'rest_framework.renderers.XMLRenderer',
        'cores.renderers.CustomXMLRenderer',
    )
}

IS_OSS_VERSION = True
#SEARCH_PAGE_HOSTNAME = "127.0.0.1"
SEARCH_PAGE_HOSTNAME = "cloudscraper-demo.homenet.org"
SEARCH_PAGE_PORT = "8000"
#SEARCH_PAGE_HOSTNAME = "cloudscraper-osse-env-2ngdpzzfhs.elasticbeanstalk.com"
#SEARCH_PAGE_PORT = "80"

#BROWSE_STARTDIR = r"c:\Users\Vojislav"
BROWSE_STARTDIR = r"c:\Users\Bratislav"

CONSTANCE_CONNECTION = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

CONSTANCE_CONFIG = {
    'SEARCH_INSIDE_KEYWORDS': (False, 'Search inside keywords'),
    'BROWSE_STARTDIR' : (r"c:\Users\Bratislav", "Start directory from where you can browse"),
    'SEARCH_PAGE_HOSTNAME' : ("192.168.0.100", 'Hostname or IP address where search page runs'),
    'SEARCH_PAGE_PORT' : (8000, 'Port where search page sends requests'),
    'LANGUAGE' : ('English', 'Laguage for user interface'),
    'SHOW_AUTHOR_IN_SNIPPETS' : (True, 'Show author info in search snippets (if available)'),
    'SHOW_YEAR_IN_SNIPPETS' : (True, 'Show year info in search snippets (if available)'),
    'SHOW_PREVIEW_IN_GOOGLEDOCS' : (True, 'Show link to preview document in google doc'),
    'PREVIEW_URL' : ('http://docs.google.com/viewer', 'Preview engine for documents'),
    'PREVIEW_URL_QUERY' : ('url=', 'Preview engine URI query'),
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

