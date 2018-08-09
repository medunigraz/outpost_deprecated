import logging
from datetime import timedelta

from celery.task import PeriodicTask

from ..campusonline.models import Organization as COOrganization
from ..campusonline.models import Person as COPerson
from ..geo.models import Room
from .models import (
    Organization,
    Person,
)

logger = logging.getLogger(__name__)


class StructureSyncTask(PeriodicTask):
    run_every = timedelta(hours=2)

    def run(self, **kwargs):
        for cop in COPerson.objects.all():
            logger.debug(f'Sync campusonline.Person {cop.pk}')
            try:
                r = Room.objects.get(campusonline=cop.room)
            except Room.DoesNotExist:
                logger.debug(f'No geo.Room for {cop}) ({cop.pk})')
                continue
            try:
                p = Person.objects.get(campusonline_id=cop.pk)
                logger.debug(f'Found {p}')
            except Person.DoesNotExist:
                p = Person(campusonline=cop)
                logger.info(f'Create {p}')
            if not p.pk or p.room.pk != r.pk:
                p.room = r
                p.save()
        for p in Person.objects.all():
            logger.debug(f'Sync structure.Person {p} ({p.pk})')
            try:
                cop = COPerson.objects.get(pk=p.campusonline_id)
                logger.debug(f'Found {cop}')
            except COPerson.DoesNotExist:
                logger.warn(f'Remove {p.pk}')
                p.delete()
        for coo in COOrganization.objects.all():
            logger.debug(f'Sync campusonline.Organization {coo} ({coo.pk})')
            try:
                o = Organization.objects.get(campusonline_id=coo.pk)
                logger.debug(f'Found {o}')
            except Organization.DoesNotExist:
                o = Organization(campusonline=coo)
                logger.info(f'Create {o}')
                o.save()
        for o in Organization.objects.all():
            logger.debug(f'Sync structure.Organization {o.pk}')
            try:
                coo = COOrganization.objects.get(pk=o.campusonline_id)
                logger.debug(f'Found {coo}')
            except COOrganization.DoesNotExist:
                logger.warn(f'Remove {o.pk}')
                o.delete()
