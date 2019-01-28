from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
)
from django.db import models

from .conf import settings


class Consumer(models.Model):
    key = models.CharField(
        max_length=max(settings.LTI_CLIENT_KEY_LENGTH),
        validators=(
            MinLengthValidator(min(settings.LTI_CLIENT_KEY_LENGTH)),
            MaxLengthValidator(max(settings.LTI_CLIENT_KEY_LENGTH)),
        ),
        primary_key=True
    )
    name = models.CharField(
        max_length=256
    )
    enabled = models.BooleanField(
        default=False
    )
    secret = models.CharField(
        max_length=256
    )
    rsa = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class History(models.Model):
    consumer = models.ForeignKey(
        'Consumer'
    )
    timestamp = models.DateTimeField()
    nonce = models.CharField(
        max_length=max(settings.LTI_NONCE_LENGTH)
    )
    token = models.CharField(
        max_length=max(settings.LTI_TOKEN_LENGTH),
        blank=True,
        null=True
    )

    class Meta:
        indexes = (
            models.Index(fields=[
                'consumer',
                'timestamp',
                'nonce',
                'token',
            ]),
        )
