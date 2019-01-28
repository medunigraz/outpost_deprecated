import os
import sys

if not hasattr(sys, 'argv'):
    setattr(sys, 'argv', [''])

from celery import Celery  # NOQA

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'outpost.django.settings')

from django.conf import settings  # NOQA

app = Celery('outpost')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
