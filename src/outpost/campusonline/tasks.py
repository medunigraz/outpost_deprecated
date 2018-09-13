import logging
from datetime import timedelta

from celery.task import PeriodicTask
from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError

from .models import Person

logger = logging.getLogger(__name__)


class UsernameSyncTask(PeriodicTask):
    run_every = timedelta(hours=1)

    def run(self, **kwargs):
        try:
            cache = caches['meduniverse']
        except InvalidCacheBackendError:
            logger.info('No meduniverse cache defined, not running UsernameSyncTask')
            return
        persons = Person.objects.all()
        id_to_username = {p.pk: p.username for p in persons}
        cache.set('id_to_username', id_to_username)
        username_to_id = {p.username: p.pk for p in persons}
        cache.set('username_to_id', username_to_id)
        for p in persons:
            cache.set(f'username:{p.username}', p.pk)
            cache.set(f'id:{p.pk}', p.username)
