import os

from appconf import AppConf
from django.conf import settings


class BaseAppConf(AppConf):
    PERS_ID_FILTER = '(CO-KAGESPERSNR-N={id})'
    PERS_FIELDS = ['cn', 'mail']

    class Meta:
        prefix = 'kages'
