import os

from appconf import AppConf
from django.conf import settings


class CAMPUSonlineAppConf(AppConf):
    BULLETIN_OCR_LANGUAGE = 'deu+eng'
    BULLETIN_OCR_DPI = 300
    BULLETIN_OCR_THRESHOLD = 50

    class Meta:
        prefix = 'campusonline'
