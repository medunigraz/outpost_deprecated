from appconf import AppConf
from django.conf import settings  # NOQA


class LTIAppConf(AppConf):
    DUMMY_CLIENT = 'dummy'
    DUMMY_SECRET = 'dummy'
    DUMMY_RSA = 'dummy'
    CLIENT_KEY_LENGTH = 6, 30
    NONCE_LENGTH = 20, 40
    NONCE_TIMEDELTA_MAX = 600
    TOKEN_LENGTH = 20, 30

    class Meta:
        prefix = 'lti'
