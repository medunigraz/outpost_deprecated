import os

from appconf import AppConf
from django.conf import settings


class OpencastAppConf(AppConf):
    API_BASE = 'https://api.entwine.example.com'
    API_USERNAME = 'user'
    API_PASSWORD = 'secret'
    LDAP_PROVIDER = 'ldap'

    class Meta:
        prefix = 'opencast'
