import logging
from datetime import timedelta

from celery.task import PeriodicTask
from django.db import connection
from celery_haystack.tasks import CeleryHaystackUpdateIndex

logger = logging.getLogger(__name__)


class RefreshViewsTask(PeriodicTask):
    run_every = timedelta(hours=1)
    query = """
    SELECT oid::regclass::text FROM pg_class WHERE relkind = 'm';
    """

    def run(self, **kwargs):
        logger.debug('Refreshing materialized views.')
        with connection.cursor() as relations:
            relations.execute(self.query)
            for rel in relations:
                logger.debug('Refresh materialized view: %s', rel)
                with connection.cursor() as refresh:
                    refresh.execute('REFRESH MATERIALIZED VIEW {}'.format(rel[0]))


class UpdateHaystackTask(PeriodicTask):
    run_every = timedelta(hours=2)

    def run(self):
        CeleryHaystackUpdateIndex().run(remove=True)
