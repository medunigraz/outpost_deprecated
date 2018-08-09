import logging
from importlib import import_module

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class BaseConfig(AppConfig):
    name = 'outpost.base'

    def ready(self):
        if settings.DEBUG:
            from debug_toolbar.panels.headers import HeadersPanel
            from debug_toolbar.settings import PANELS_DEFAULTS
            HeadersPanel.ENVIRON_FILTER.add('GEOIP_ADDR')
            HeadersPanel.ENVIRON_FILTER.add('GEOIP_CONTINENT_CODE')
            HeadersPanel.ENVIRON_FILTER.add('GEOIP_COUNTRY_CODE')
            HeadersPanel.ENVIRON_FILTER.add('GEOIP_COUNTRY_NAME')
            PANELS_DEFAULTS += [
                'django_uwsgi.panels.UwsgiPanel'
            ]
        for app in settings.INSTALLED_APPS:
            try:
                plugin = import_module(f'{app}.plugins')
                logger.debug(f'Loaded plugins from {app}: {plugin}')
            except ModuleNotFoundError as e:
                # Ignore all failed imports
                pass
