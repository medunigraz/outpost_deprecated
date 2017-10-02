import logging
from datetime import timedelta

from celery.task import PeriodicTask
from celery_haystack.tasks import CeleryHaystackUpdateIndex

from .models import NetworkedDeviceMixin

logger = logging.getLogger(__name__)


class RefreshMaterializedViewsTask(PeriodicTask):
    run_every = timedelta(hours=1)
    query = '''
    SELECT oid::regclass::text FROM pg_class WHERE relkind = 'm';
    '''

    def run(self, **kwargs):
        from django.db import connection
        logger.debug('Refreshing materialized views.')
        with connection.cursor() as relations:
            relations.execute(self.query)
            for (rel,) in relations:
                logger.debug('Refresh materialized view: %s', rel)
                with connection.cursor() as refresh:
                    refresh.execute('REFRESH MATERIALIZED VIEW {}'.format(rel))
        connection.close()


class RefreshNetworkedDeviceTask(PeriodicTask):
    run_every = timedelta(minutes=2)

    def run(self, **kwargs):
        for cls in NetworkedDeviceMixin.__subclasses__():
            for obj in cls.objects.filter(enabled=True):
                obj.update()


class UpdateHaystackTask(PeriodicTask):
    run_every = timedelta(hours=2)

    def run(self):
        CeleryHaystackUpdateIndex().run(remove=True)
