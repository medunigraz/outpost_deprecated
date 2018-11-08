import logging
from textwrap import shorten

from django.contrib.gis.db import models
from django.contrib.postgres.fields import (
    ArrayField,
    HStoreField,
)

logger = logging.getLogger(__name__)


class Publication(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of doctoral school.

    ### `emails` (`string[]`)
    Contact emails.
    '''
    person = models.ForeignKey(
        'campusonline.Person',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='publications'
    )
    quote = models.TextField()
    authors = ArrayField(
        models.CharField(
            max_length=256,
            blank=True,
            null=True
        )
    )
    urls = HStoreField()
    type = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    year = models.PositiveSmallIntegerField()
    document = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    presentation = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    def __str__(self):
        return shorten(self.quote, 30)
