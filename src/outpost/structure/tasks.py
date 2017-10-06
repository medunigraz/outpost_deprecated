import logging
from datetime import timedelta

from celery.task import PeriodicTask

from ..campusonline.models import Person as COPerson
from ..campusonline.models import Organization as COOrganization
from ..geo.models import Room
from .models import Person, Organization

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
            if not p.pk or p.room.pk != r.pk:
                p.room = r
                p.save()
        for p in Person.objects.all():
            try:
                COPerson.objects.get(pk=p.campusonline_id)
            except COPerson.DoesNotExist:
                logger.debug('Remove {}'.format(p.pk))
                p.delete()
        for coo in COOrganization.objects.all():
            logger.debug('Sync campusonline.Organization {}'.format(coo))
            try:
                o = Organization.objects.get(campusonline_id=coo.pk)
                logger.debug('Found {}'.format(o))
            except Organization.DoesNotExist:
                o = Organization(campusonline=coo)
                logger.debug('Create {}'.format(o))
                o.save()
        for o in Organization.objects.all():
            try:
                COOrganization.objects.get(pk=o.campusonline_id)
            except COOrganization.DoesNotExist:
                logger.debug('Remove {}'.format(o.pk))
                o.delete()
