from datetime import timedelta
from secrets import token_urlsafe

from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
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
        default=timedelta(hours=6),
        validators=[
            MaxValueValidator(timedelta(hours=24)),
            MinValueValidator(timedelta(hours=1))
        ]
    )
    purpose = models.TextField()

    @property
    def expires(self):
        return self.created + self.lifetime

    def __str__(self):
        return '{s.user}: {s.pk}'.format(s=self)


class Login(models.Model):
    username = models.CharField(
        max_length=256,
        default=''
    )
    password = models.CharField(
        max_length=256,
        default=''
    )
    response = models.CharField(
        max_length=256,
        default=''
    )
    created = models.DateTimeField()
