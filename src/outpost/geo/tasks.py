import logging

from datetime import timedelta
from celery.task import PeriodicTask

from .models import (
    Room,
)

logger = logging.getLogger(__name__)


class GeoSyncTask(PeriodicTask):
    run_every = timedelta(hours=2)

    def run(self, **kwargs):
        rooms = Room.objects.exclude(campusonline__organization=None)
        logger.info('Synchronizing {} geo.Room'.format(rooms.count()))
        for r in rooms:
            o = Organization.objects.get(campusonline=r.campusonline.organization)
            r.organization = o
            r.save()
