import logging
from datetime import timedelta

from celery.task import PeriodicTask

from ..campusonline.models import Person as COPerson
from ..geo.models import Room
from .models import Person

logger = logging.getLogger(__name__)


class StructureSyncTask(PeriodicTask):
    run_every = timedelta(hours=2)

    def run(self, **kwargs):
        for cop in COPerson.objects.all():
            logger.debug('Sync campusonline.Person {}'.format(cop))
            try:
                r = Room.objects.get(campusonline=cop.room)
            except Room.DoesNotExist:
                logger.debug('No geo.Room for {}'.format(cop))
                continue
            try:
                p = Person.objects.get(campusonline_id=cop.pk)
                logger.debug('Found {}'.format(p))
            except Person.DoesNotExist:
                p = Person(campusonline=cop)
                logger.debug('Create {}'.format(p))
            p.room = r
            p.save()
