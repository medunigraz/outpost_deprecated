import logging
from datetime import timedelta

from celery.task import PeriodicTask

from outpost.django.campusonline.models import Organization as COOrganization
from outpost.django.campusonline.models import Person as COPerson
from outpost.django.geo.models import Room

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
            p, created = Person.objects.get_or_create(
                campusonline_id=cop.pk,
                defaults={
                    'campusonline': cop
                }
            )
            if created:
                logger.info(f'Create {p}')
            else:
                logger.debug(f'Found {p}')
            if cop.room:
                try:
                    r = Room.objects.get(campusonline=cop.room)
                    if not p.room:
                        p.room = r
                        p.save()
                    else:
                        if p.room.pk != r.pk:
                            p.room = r
                            p.save()
                except Room.DoesNotExist:
                    logger.debug(f'No geo.Room for {cop}) ({cop.pk})')
        for p in Person.objects.all().order_by('pk'):
            logger.debug(f'Sync structure.Person {p.pk}')
            try:
                cop = COPerson.objects.get(pk=p.campusonline_id)
                logger.debug(f'Found {cop}')
            except COPerson.DoesNotExist:
                logger.warn(f'Remove {p.pk}')
                p.delete()
        for coo in COOrganization.objects.all():
            logger.debug(f'Sync campusonline.Organization {coo} ({coo.pk})')
            o, created = Organization.objects.get_or_create(
                campusonline_id=coo.pk,
                defaults={
                    'campusonline': coo
                }
            )
            if created:
                logger.info(f'Create {o}')
            else:
                logger.debug(f'Found {o}')
        for o in Organization.objects.all().order_by('pk'):
            logger.debug(f'Sync structure.Organization {o.pk}')
            try:
                coo = COOrganization.objects.get(pk=o.campusonline_id)
                logger.debug(f'Found {coo}')
            except COOrganization.DoesNotExist:
                logger.warn(f'Remove {o.pk}')
                o.delete()
