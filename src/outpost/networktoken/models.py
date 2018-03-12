from datetime import timedelta
from secrets import token_urlsafe

from django.conf import settings
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel


class Token(TimeStampedModel):

    def generate():
        return token_urlsafe(7)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    value = models.CharField(
        max_length=10,
        default=generate
    )
    lifetime = models.DurationField(
        default=timedelta(hours=6)
    )

    @property
    def expires(self):
        return self.created + self.lifetime

    def __str__(self):
        return '{s.user}: {s.pk}'.format(s=self)