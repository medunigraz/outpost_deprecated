from django.apps import AppConfig

fromd jango.conf import settings


default_app_config = 'outpost.base.apps.BaseConfig'


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        if settings.DEBUG:
            from debug_toolbar.panels.headers import HeadersPanel
            HeadersPanel.ENVIRON_FILTER.add('GEOIP_ADDR')
            HeadersPanel.ENVIRON_FILTER.add('GEOIP_CONTINENT_CODE')
            HeadersPanel.ENVIRON_FILTER.add('GEOIP_COUNTRY_CODE')
            HeadersPanel.ENVIRON_FILTER.add('GEOIP_COUNTRY_NAME')
