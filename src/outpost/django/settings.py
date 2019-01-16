'''
Django settings for Outpost project.
'''

import os

import ldap
import saml2
import saml2.attributemaps
import saml2.saml
from corsheaders.defaults import default_methods
from django.utils.translation import ugettext_lazy as _
from django_auth_ldap.config import (
    GroupOfNamesType,
    LDAPSearch,
)
from docutils.core import publish_parts
from geopy.geocoders import Nominatim

BASE_DIR = os.path.abspath(os.path.join(__file__, '../../../..'))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', None)

SITE_ID = os.environ.get('DJANGO_SITE_ID', None)

DEBUG = False

ADMINS = tuple()

EMAIL_HOST = 'localhost'
SERVER_EMAIL = 'it-server@medunigraz.at'

INTERNAL_IPS = list()

ALLOWED_HOSTS = list()

INSTALLED_APPS = [
    'channels',
    'django_dbconn_retry',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.gis',
    'django.contrib.sites',
    'django.contrib.admin',
    'outpost.django.base',
    'outpost.django.api',
    'outpost.django.attendance',
    'outpost.django.campusonline',
    'outpost.django.geo',
    'outpost.django.networktoken',
    'outpost.django.oauth2',
    'outpost.django.positioning',
    'outpost.django.research',
    'outpost.django.restaurant',
    'outpost.django.salt',
    'outpost.django.structure',
    'outpost.django.thesis',
    'outpost.django.typo3',
    'outpost.django.video',
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
    # 'dynamic_scraper',
    'haystack',
    'polymorphic',
    'push_notifications',
    'ordered_model',
    'django_celery_results',
    'celery_haystack',
    'rules.apps.AutodiscoverRulesConfig',
    'overextends',
    'netfields',
    'imagekit',
    'taggit',
    'memoize',
    'django_filters',
    'rest_hooks',
    'django_prometheus',
    'djangosaml2',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    # 'django_downloadview.SmartDownloadMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'outpost.django.urls'

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

WSGI_APPLICATION = 'outpost.django.wsgi.application'
ASGI_APPLICATION = "outpost.django.asgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'development.db')
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    },
    'meduniverse': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                ('localhost', 6379)
            ],
        },
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CSRF_COOKIE_SECURE = True

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
    ('text/less', 'outpost.django.compressor.DjangoLessFilter'),
    ('text/x-scss', 'django_pyscss.compressor.DjangoScssFilter'),
]

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'base:index'
LOGOUT_REDIRECT_URL = '/'

SAML_CREATE_UNKNOWN_USER = True
SAML_ATTRIBUTE_MAPPING = {
    'uid': ('username', ),
}
SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_POST
SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
    'xmlsec_binary': '/usr/bin/xmlsec1',

    # your entity id, usually your subdomain plus the url to the metadata view
    'entityid': 'http://localhost:8000/saml2/metadata/',

    # directory with attribute mapping
    'attribute_map_dir': os.path.dirname(saml2.attributemaps.__file__),

    # this block states what services we provide
    'service': {
        # we are just a lonely SP
        'sp': {
            'name': 'Federated Django sample SP',
            'name_id_format': saml2.saml.NAMEID_FORMAT_PERSISTENT,
            'endpoints': {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                'assertion_consumer_service': [
                    (
                        'http://localhost:8000/saml2/acs/',
                        saml2.BINDING_HTTP_POST
                    ),
                ],
                # url and binding to the single logout service view
                # do not change the binding or service name
                'single_logout_service': [
                    (
                        'http://localhost:8000/saml2/ls/',
                        saml2.BINDING_HTTP_REDIRECT
                    ),
                    (
                        'http://localhost:8000/saml2/ls/post',
                        saml2.BINDING_HTTP_POST
                    ),
                ],
            },

            # attributes that this project need to identify a user
            'required_attributes': ['uid'],

            # attributes that may be useful to have but not required
            'optional_attributes': ['eduPersonAffiliation'],

            # in this section the list of IdPs we talk to are defined
            'idp': {
                # we do not need a WAYF service since there is
                # only an IdP defined here. This IdP should be
                # present in our metadata

                # the keys of this dictionary are entity ids
                'https://localhost/simplesaml/saml2/idp/metadata.php': {
                    'single_sign_on_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://localhost/simplesaml/saml2/idp/SSOService.php',
                    },
                    'single_logout_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://localhost/simplesaml/saml2/idp/SingleLogoutService.php',
                    },
                },
            },
        },
    },

    # where the remote metadata is stored
    'metadata': {
        'local': [os.path.join(BASE_DIR, 'remote_metadata.xml')],
    },

    # set to 1 to output debugging information
    'debug': 1,

    # Signing
    'key_file': os.path.join(BASE_DIR, 'mycert.key'),  # private part
    'cert_file': os.path.join(BASE_DIR, 'mycert.pem'),  # public part

    # Encryption
    'encryption_keypairs': [{
        'key_file': os.path.join(BASE_DIR, 'my_encryption_key.key'),  # private part
        'cert_file': os.path.join(BASE_DIR, 'my_encryption_cert.pem'),  # public part
    }],

    # own metadata settings
    'contact_person': [
        {
            'given_name': 'Lorenzo',
            'sur_name': 'Gil',
            'company': 'Yaco Sistemas',
            'email_address': 'lgs@yaco.es',
            'contact_type': 'technical'
        },
        {
            'given_name': 'Angel',
            'sur_name': 'Fernandez',
            'company': 'Yaco Sistemas',
            'email_address': 'angel@yaco.es',
            'contact_type': 'administrative'
        },
    ],
    # you can set multilanguage information here
    'organization': {
        'name': [
            ('Yaco Sistemas', 'es'),
            ('Yaco Systems', 'en'),
        ],
        'display_name': [
            ('Yaco', 'es'),
            ('Yaco', 'en'),
        ],
        'url': [
            ('http://www.yaco.es', 'es'),
            ('http://www.yaco.com', 'en'),
        ],
    },
    'valid_for': 24,  # how long is our metadata valid
}

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
    'oauth2_provider.backends.OAuth2Backend',
    'djangosaml2.backends.Saml2Backend',
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
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=users,dc=example,dc=com",
    ldap.SCOPE_SUBTREE,
    "(uid=%(user)s)"
)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "ou=django,ou=groups,dc=example,dc=com",
    ldap.SCOPE_SUBTREE,
    "(objectClass=groupOfNames)"
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
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_METADATA_CLASS': 'outpost.django.api.metadata.ExtendedMetadata',
}

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 3600
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'api.medunigraz.at',
    }
}

HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'
CELERY_HAYSTACK_DEFAULT_TASK = 'outpost.django.base.tasks.LockedCeleryHaystackSignalHandler'
CELERY_HAYSTACK_QUEUE = 'haystack'

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups',
        'editor': 'Edit objects',
        'geo': _('Manage geopgraphic information'),
        'media': _('Manage multimedia data'),
        'holding': _('Manage holdings'),
    }
}
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2.Application'


CORS_ORIGIN_ALLOW_ALL = True
CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_METHODS = default_methods + (
    'START',
    'STOP',
)

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

RADIUS_USER = 'radius'

CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULTS_BACKEND = 'django-db'
CELERY_TASK_DEFAULT_QUEUE = 'default'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

HOOK_DELIVERER = 'outpost.django.base.hooks.deliver_hook_wrapper'
HOOK_EVENTS = {}

RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8088'

GEORESOLVERS = (
    Nominatim(user_agent=__package__),
)

OUTPOST = {
    'epiphan_provisioning': False,
    'typo3_api': 'https://localhost/api/',
    'typo3_fileadmin': 'https://localhost/fileadmin',
    'nconvert': '/usr/local/bin/nconvert',
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
        __package__: {
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
