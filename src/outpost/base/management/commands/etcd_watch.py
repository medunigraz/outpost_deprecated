'''
Django settings for MEDUNIGRAZ project.
'''

from importlib import import_module
from pathlib import Path
from pprint import PrettyPrinter
from urllib.parse import parse_qsl

from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from etcd import Client


class Command(BaseCommand):
    help = 'Touch WSGI file everytime a setting in ETCD is changed.'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='*', type=str)

    def handle(self, *args, **options):
        pp = PrettyPrinter(indent=4)
        pp.pprint(options)
        u = settings.ETCD_URL
        m = '.'.join(settings.WSGI_APPLICATION.split('.')[:-1])
        p = Path(import_module(m).__file__)
        c = Client(
            protocol=u.scheme,
            host=u.hostname,
            port=u.port,
            username=u.username,
            password=u.password,
            **dict(parse_qsl(u.query))
        )
        while True:
            print('Waiting for settings to change.')
            c.read(
                u.path,
                recursive=True,
                wait=True,
                timeout=0
            )
            print('Touching file.')
            p.touch()
