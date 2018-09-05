import logging
from datetime import timedelta

from celery.task import (
    PeriodicTask,
    Task,
)
from celery.task.schedules import crontab
from django.db.models import Q
from django.utils import timezone

from .models import (
    CampusOnlineEntry,
    Holding,
    Terminal,
)

logger = logging.getLogger(__name__)


class CampusOnlineEntryCleanUpTask(PeriodicTask):
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


class HoldingCleanUpTask(PeriodicTask):
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):
        # TODO: Fix filter to find holding that have recently ended
        for h in Holding.objects.filter(state='running'):
            h.end()
            h.save()
