from django.db import models


class GroupMap(models.Model):
    group = models.CharField(
        max_length=128
    )
    dn = models.CharField(
        max_length=512
    )
    filter = models.TextField(
        blank=True,
        null=True
    )
    enabled = models.BooleanField(
        default=False
    )
    username_field = models.CharField(
        max_length=128
    )
    email_field = models.CharField(
        max_length=128
    )

    def __str__(self):
        return self.group
