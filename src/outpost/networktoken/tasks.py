import logging
from datetime import timedelta

from django.utils import timezone
from django.db import models
from celery.task.schedules import crontab
from celery.task import PeriodicTask

from outpost.base.tasks import MaintainanceTaskMixin

from .models import (
    Token,
)

logger = logging.getLogger(__name__)


class TokenCleanupTask(MaintainanceTaskMixin, PeriodicTask):
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):
        logger.debug('Running cleanup for expired network tokens')
        Token.objects.annotate(
            eol=models.ExpressionWrapper(
                F('created') + F('lifetime'),
                output=models.DateTimeField()
            )
        ).filter(eol_lte=timezone.now()).delete()
