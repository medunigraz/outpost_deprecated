'''
Django settings for Outpost project.
'''

import json
import os

import ldap
import raven
from django_auth_ldap.config import (
    GroupOfNamesType,
    LDAPSearch,
)
from docutils.core import publish_parts

BASE_DIR = os.path.abspath(os.path.join(__file__, '../../..'))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', None)

SITE_ID = os.environ.get('DJANGO_SITE_ID', None)

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
    'django.contrib.sites',
    'outpost.base',
    'outpost.api',
    'outpost.campusonline',
    'outpost.positioning',
    'outpost.geo',
    'outpost.attendance',
    'outpost.typo3',
    'outpost.oauth2',
    'outpost.video',
    'outpost.structure',
    'django.contrib.admin',
    'django_extensions',
    'crispy_forms',
    'guardian',
    'reversion',
    'compressor',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'oauth2_provider',
    'corsheaders',
    'social.apps.django_app.default',
    #'dynamic_scraper',
    'haystack',
    'polymorphic',
    'push_notifications',
    'ordered_model',
    'django_celery_results',
    'celery_haystack',
    'rules.apps.AutodiscoverRulesConfig',
    'overextends',
    'netfields',
    'raven.contrib.django.raven_compat',
    'imagekit',
    'taggit',
    'django_uwsgi',
    'memoize',
    'django_filters',
]

MIDDLEWARE = [
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    #'django_downloadview.SmartDownloadMiddleware',
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
            'builtins': [
                'overextends.templatetags.overextends_tags',
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

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

COMPRESS_PRECOMPILERS = [
    ('text/less', 'outpost.compressor.DjangoLessFilter'),
    ('text/x-scss', 'django_pyscss.compressor.DjangoScssFilter'),
]

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'base:index'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
    'oauth2_provider.backends.OAuth2Backend',
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

AUTH_LDAP_SERVER_URI = "ldap://ldap.example.com"
AUTH_LDAP_BIND_DN = "cn=django-agent,dc=example,dc=com"
AUTH_LDAP_BIND_PASSWORD = "phlebotinum"
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,dc=example,dc=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=django,ou=groups,dc=example,dc=com",
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")
AUTH_LDAP_REQUIRE_GROUP = "cn=enabled,ou=django,ou=groups,dc=example,dc=com"
AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=django,ou=groups,dc=example,dc=com"
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}
AUTH_LDAP_PROFILE_ATTR_MAP = {
    "employee_number": "employeeNumber"
}
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
    "is_staff": "cn=staff,ou=django,ou=groups,dc=example,dc=com",
    "is_superuser": "cn=superuser,ou=django,ou=groups,dc=example,dc=com"
}
AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
    "is_awesome": "cn=awesome,ou=django,ou=groups,dc=example,dc=com",
}
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_METADATA_CLASS': 'outpost.api.metadata.ExtendedMetadata',
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

HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups',
        'editor': 'Edit objects',
    }
}
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2.Application'


CORS_ORIGIN_ALLOW_ALL = True
CORS_REPLACE_HTTPS_REFERER = True

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

CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULTS_BACKEND = 'django-db'
CELERY_TASK_DEFAULT_QUEUE = 'default'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8088'

OUTPOST = {
    'epiphan_provisioning': False,
    'typo3_api': 'https://localhost/api/',
}

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
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'graypy': {
            'level': 'WARNING',
            'class': 'graypy.GELFHandler',
            'host': 'graylog.medunigraz.at',
            'port': 12201,
        },
    },
    'loggers': {
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'graypy'],
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['graypy'],
            'level': 'ERROR',
            'propagate': True,
        },
        'rules': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'outpost': {
            'handlers': ['console', 'mail_admins'],
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
