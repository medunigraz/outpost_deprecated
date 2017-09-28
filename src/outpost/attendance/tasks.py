import logging
from datetime import timedelta

from django.db.models import Q
from celery.task.schedules import crontab
from celery.task import (
    PeriodicTask,
    Task,
)

from .models import (
    Holding,
    Terminal,
    Entry,
)

logger = logging.getLogger(__name__)


class EntryCleanUpTask(PeriodicTask):
    run_every = crontab(hour=0, minute=0)

    def run(self, **kwargs):
        cond = Q(state='registered') | Q(state='assigned')
        for e in Entry.objects.filter(cond):
            if e.state == 'registered':
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


class TerminalOnlineTask(PeriodicTask):
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):
        terminals = Terminal.objects.filter(enabled=True)
        logger.info('Pinging {} terminals.'.format(terminals.count()))

        for t in terminals:
            t.update()

