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
    refresh = '''
    REFRESH MATERIALIZED VIEW {};
    '''

    def run(self, **kwargs):
        from django.db import connection
        from ..fdw import OutpostFdw
        logger.debug('Refreshing materialized views.')
        with connection.cursor() as relations:
            relations.execute(self.views)
            for (rel,) in relations:
                logger.debug('Refresh materialized view: %s', rel)
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
                        with connection.cursor() as refresh:
                            refresh.execute(self.refresh.format(rel))
                    else:
                        logger.warn(
                            'Could not refresh materialized view: {}'.format(rel)
                        )
        connection.close()


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
