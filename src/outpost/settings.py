'''
Django settings for Outpost project.
'''

import json
import os

from docutils.core import publish_parts


BASE_DIR = os.path.abspath(os.path.join(__file__, '../../..'))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', None)

DEBUG = False

ADMINS = tuple()

EMAIL_HOST = 'localhost'
SERVER_EMAIL = 'it-server@medunigraz.at'

INTERNAL_IPS = list()

ALLOWED_HOSTS = list()

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'outpost.base',
    'outpost.geo',
    'outpost.attendance',
    'django.contrib.admin',
    'django_extensions',
    'crispy_forms',
    'guardian',
    'django_python3_ldap',
    'reversion',
    'compressor',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'oauth2_provider',
    'corsheaders',
    'social.apps.django_app.default',
    'djoser',
    #'dynamic_scraper',
    'haystack',
    'polymorphic',
    'redis_admin',
    'push_notifications',
    'ordered_model',
]

MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'stronghold.middleware.LoginRequiredMiddleware',
    # 'reversion.middleware.RevisionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django_downloadview.SmartDownloadMiddleware',
]

ROOT_URLCONF = 'outpost.urls'

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
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'outpost.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'development.db')
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

COMPRESS_PRECOMPILERS = [
    ('text/less', 'outpost.compressor.DjangoLessFilter'),
    ('text/x-scss', 'django_pyscss.compressor.DjangoScssFilter'),
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'django_python3_ldap.auth.LDAPBackend',
    'guardian.backends.ObjectPermissionBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# The URL of the LDAP server.
LDAP_AUTH_URL = 'ldap://localhost:389'

# Initiate TLS on connection.
LDAP_AUTH_USE_TLS = False

# The LDAP search base for looking up users.
LDAP_AUTH_SEARCH_BASE = 'dc=example,dc=com'

# The LDAP class that represents a user.
LDAP_AUTH_OBJECT_CLASS = 'inetOrgPerson'

# User model fields mapped to the LDAP
# attributes that represent them.
LDAP_AUTH_USER_FIELDS = {
    'username': 'cn',
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

# A tuple of django model fields used to uniquely identify a user.
LDAP_AUTH_USER_LOOKUP_FIELDS = ('username',)

# Path to a callable that takes a dict of {model_field_name: value},
# returning a dict of clean model data.
# Use this to customize how data loaded from LDAP is saved to the User model.
LDAP_AUTH_CLEAN_USER_DATA = 'django_python3_ldap.utils.clean_user_data'

# Path to a callable that takes a user model and a dict of {ldap_field_name:
# [value]}, and saves any additional user relationships based on the LDAP data.
# Use this to customize how data loaded from LDAP is saved to User model
# relations. For customizing non-related User model fields, use
# LDAP_AUTH_CLEAN_USER_DATA.
LDAP_AUTH_SYNC_USER_RELATIONS = 'django_python3_ldap.utils.sync_user_relations'

# Path to a callable that takes a dict of {ldap_field_name: value},
# returning a list of [ldap_search_filter]. The search filters will then be
# AND'd together when creating the final search filter.
LDAP_AUTH_FORMAT_SEARCH_FILTERS = 'outpost.ldap.group_membership_filter'

# Path to a callable that takes a dict of {model_field_name: value}, and
# returns a string of the username to bind to the LDAP server. Use this to
# support different types of LDAP server.
LDAP_AUTH_FORMAT_USERNAME = 'django_python3_ldap.utils.format_username_openldap'

# Sets the login domain for Active Directory users.
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = None

# The LDAP username and password of a user for authenticating the
# `ldap_sync_users` management command. Set to None if you allow anonymous
# queries.
LDAP_AUTH_CONNECTION_USERNAME = None
LDAP_AUTH_CONNECTION_PASSWORD = None

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS': None,
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 15
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'api.medunigraz.at',
    }
}

CORS_ORIGIN_ALLOW_ALL = True

DEFAULT_SRID = 3857

MARKUP_FIELD_TYPES = [
    ('ReST', lambda markup: publish_parts(source=markup, writer_name='html5')['body'])
]

DOWNLOADVIEW_BACKEND = 'django_downloadview.apache.XSendfileMiddleware'

DOWNLOADVIEW_RULES = [
    {
        'source_url': '/media/apache/',
        'destination_dir': '/apache-optimized-by-middleware/'
    }
]

RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8088'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django_python3_ldap': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

if 'DJANGO_LOCAL_CONFIGURATION' in os.environ:
    filename = os.path.abspath(os.environ.get('DJANGO_LOCAL_CONFIGURATION'))
    if os.access(filename, os.R_OK):
        with open(filename) as config:
            code = compile(config.read(), filename, 'exec')
            exec(code, globals(), locals())
