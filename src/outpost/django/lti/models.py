import json

from django.contrib.auth.models import Group
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
)
from django.db import models
from polymorphic.models import PolymorphicModel
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer

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


class GroupRole(models.Model):
    role = models.CharField(
        primary_key=True,
        max_length=256
    )
    group = models.ForeignKey(
        Group
    )

    def __str__(self):
        return f'{self.role}: {self.group}'


class Resource(PolymorphicModel):
    consumer = models.ForeignKey(
        'Consumer',
        on_delete=models.CASCADE
    )
    resource = models.CharField(
        max_length=256
    )


class DebugResource(Resource):
    formater = HtmlFormatter()

    def render(self, user, params):
        data = {
            'style': self.formater.get_style_defs('.highlight'),
            'json': highlight(
                json.dumps(dict(params), indent=2),
                JsonLexer(),
                self.formater
            ),
        }
