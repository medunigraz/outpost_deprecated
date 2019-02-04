import os

from appconf import AppConf
from django.conf import settings


class CAMPUSonlineAppConf(AppConf):
    BULLETIN_OCR_LANGUAGE = 'deu+eng'

    class Meta:
        prefix = 'campusonline'
