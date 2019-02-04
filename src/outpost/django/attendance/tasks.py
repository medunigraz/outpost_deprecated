import logging
from datetime import timedelta

from celery.task import (
    PeriodicTask,
    Task,
)
from celery.task.schedules import crontab
from django.db.models import Q
from django.utils import timezone

from outpost.campusonline.models import Student

from .models import (
    CampusOnlineEntry,
    CampusOnlineHolding,
    Entry,
    Terminal,
)

logger = logging.getLogger(__name__)


class EntryCleanupTask(PeriodicTask):
    run_every = timedelta(minutes=15)

    def run(self, **kwargs):
        for e in Entry.objects.all():
            try:
                Student.objects.get(pk=e.student_id)
            except Student.DoesNotExist:
                logger.warn(f'Removing student {e.student_id} link for entry {e.pk}')
                if not e.status:
                    e.status = dict()
                e.status['student'] = e.student_id
                e.student = None
                e.save()


class CampusOnlineEntryCleanupTask(PeriodicTask):
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):
        past = timezone.now() - timedelta(hours=12)
        cond = (Q(state='created') & Q(incoming__created__lt=past)) | (Q(state='assigned') & Q(assigned__lt=past))
        for e in CampusOnlineEntry.objects.filter(cond):
            if e.state == 'created':
                e.cancel()
            if e.state == 'assigned':
                e.leave()
            e.save()


class HoldingCleanupTask(PeriodicTask):
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):
        # TODO: Fix filter to find holding that have recently ended
        for h in CampusOnlineHolding.objects.filter(state='running'):
            h.end()
            h.save()
