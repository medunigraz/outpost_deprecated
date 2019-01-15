import logging
from textwrap import shorten

from django.contrib.gis.db import models
from django.contrib.postgres.fields import (
    ArrayField,
    HStoreField,
)
from memoize import memoize

logger = logging.getLogger(__name__)


class Category(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of doctoral school.

    ### `emails` (`string[]`)
    Contact emails.
    '''
    name = HStoreField()

    class Meta:
        managed = False
        db_table = 'research_category'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class Document(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of doctoral school.

    ### `emails` (`string[]`)
    Contact emails.
    '''
    name = HStoreField()

    class Meta:
        managed = False
        db_table = 'research_document'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


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
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    authors = ArrayField(
        models.CharField(
            max_length=256,
        )
    )
    year = models.PositiveSmallIntegerField()
    source = models.TextField()
    category = models.ForeignKey(
        'Category',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    document = models.ForeignKey(
        'Document',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    sci = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    pubmed = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    doi = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    pmc = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    abstract_bytes = models.BinaryField(
        blank=True,
        null=True,
    )
    persons = models.ManyToManyField(
        'campusonline.Person',
        db_table='research_publication_person',
        db_constraint=False,
        related_name='publications'
    )
    organizations = models.ManyToManyField(
        'campusonline.Organization',
        db_table='research_publication_organization',
        db_constraint=False,
        related_name='publications'
    )

    class Meta:
        managed = False
        db_table = 'research_publication'

    class Refresh:
        interval = 86400

    @property
    #@memoize(timeout=3600)
    def abstract(self):
        if not self.abstract_bytes:
            return None
        return self.abstract_bytes.tobytes().decode('utf-8').strip()

    def __repr__(self):
        return str(self.pk)

    def __str__(self):
        if not self.abstract_bytes:
            return str(self.pk)
        short = shorten(self.abstract, 30)
        return f'{self.pk}: {short}'
