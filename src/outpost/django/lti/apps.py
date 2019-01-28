import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class LTIConfig(AppConfig):
    name = 'outpost.django.lti'
