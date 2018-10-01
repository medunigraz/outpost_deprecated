import logging
from datetime import timedelta

from celery.task import PeriodicTask
from celery_haystack.tasks import CeleryHaystackUpdateIndex
from guardian.utils import clean_orphan_obj_perms
from sqlalchemy.exc import DBAPIError

from .models import NetworkedDeviceMixin

logger = logging.getLogger(__name__)


class MaintainanceTaskMixin:
    options = {
        'queue': 'maintainance'
    }
    queue = 'maintainance'


class RefreshMaterializedViewsTask(MaintainanceTaskMixin, PeriodicTask):
    run_every = timedelta(hours=1)
    views = '''
    SELECT oid::regclass::text FROM pg_class WHERE relkind = 'm';
    '''
    wrappers = '''
    SELECT
        cl_d.relname AS name,
        ns.nspname AS schema,
        ft.ftoptions AS options
    FROM pg_rewrite AS r
    JOIN pg_class AS cl_r ON r.ev_class = cl_r.oid
    JOIN pg_depend AS d ON r.oid = d.objid
    JOIN pg_class AS cl_d ON d.refobjid = cl_d.oid
    JOIN pg_namespace AS ns ON cl_d.relnamespace = ns.oid
    JOIN pg_foreign_table AS ft ON ft.ftrelid = cl_d.oid
    JOIN pg_foreign_server AS fs ON fs.oid = ft.ftserver
    WHERE
        cl_d.relkind = 'f' AND
        cl_r.relname='{}' AND
        fs.srvname = 'sqlalchemy'
    GROUP BY
        cl_d.relname,
        ns.nspname,
        ft.ftoptions
    ORDER BY
        ns.nspname,
        cl_d.relname;
    '''
    indizes = '''
    SELECT
        COUNT(1) AS count
    FROM
        pg_indexes
    WHERE
        tablename = '{}' AND
        indexdef LIKE 'CREATE UNIQUE INDEX %'
    '''
    refresh_default = '''
    REFRESH MATERIALIZED VIEW {};
    '''
    refresh_concurrent = '''
    REFRESH MATERIALIZED VIEW CONCURRENTLY {};
    '''

    def run(self, **kwargs):
        from django.db import connection
        from ..fdw import OutpostFdw
        logger.debug('Refreshing materialized views.')
        with connection.cursor() as relations:
            relations.execute(self.views)
            for (rel,) in relations:
                logger.debug(f'Refresh materialized view: {rel}')
                with connection.cursor() as check:
                    check.execute(self.wrappers.format(rel))
                    online = True
                    for (name, schema, options) in check:
                        if options:
                            args = dict([o.split('=', 1) for o in options])
                            try:
                                OutpostFdw(args, {}).connection.connect()
                            except DBAPIError as e:
                                logger.warn(e)
                                online = False
                    if online:
                        with connection.cursor() as indizes:
                            indizes.execute(self.indizes.format(rel))
                            (index,) = indizes.fetchone()
                        self.refresh(rel, index > 0)
                    else:
                        logger.warn(f'Could not refresh materialized view: {rel}')
        connection.close()

    def refresh(self, name, concurrent=False):
        from django.db import (
            connection,
            IntegrityError,
            ProgrammingError,
            transaction
        )
        try:
            with transaction.atomic():
                with connection.cursor() as refresh:
                    if concurrent:
                        logger.debug(f'Concurrent refresh: {name}')
                        refresh.execute(self.refresh_concurrent.format(name))
                    else:
                        logger.debug(f'Refresh: {name}')
                        refresh.execute(self.refresh_default.format(name))
        except (IntegrityError, ProgrammingError) as e:
            logger.error(e)



class RefreshNetworkedDeviceTask(MaintainanceTaskMixin, PeriodicTask):
    run_every = timedelta(minutes=2)

    def run(self, **kwargs):
        for cls in NetworkedDeviceMixin.__subclasses__():
            for obj in cls.objects.filter(enabled=True):
                obj.update()


class UpdateHaystackTask(MaintainanceTaskMixin, PeriodicTask):
    run_every = timedelta(hours=2)

    def run(self):
        CeleryHaystackUpdateIndex().run(remove=True)


class CleanUpPermsTask(MaintainanceTaskMixin, PeriodicTask):
    run_every = timedelta(hours=1)

    def run(self):
        clean_orphan_obj_perms()
