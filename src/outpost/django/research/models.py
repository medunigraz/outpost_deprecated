import logging
import re
from textwrap import shorten

from django.contrib.gis.db import models
from django.contrib.postgres.fields import (
    ArrayField,
    HStoreField,
)
from memoize import memoize

logger = logging.getLogger(__name__)


class Country(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of country, defined by language.

    ### `iso` (`string`)
    ISO code of country.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    iso = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'research_country'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class Language(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of language.

    ### `iso` (`string`)
    ISO code of language.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    iso = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'research_language'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class FunderCategory(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of funder category, defined by language.

    ### `short` (`string`)
    Short name of funder category.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    short = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'research_fundercategory'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class Funder(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of funder, defined by language.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    street = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    zipcode = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    country = models.ForeignKey(
        'Country',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    url = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        'FunderCategory',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = 'research_funder'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class ProjectCategory(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project Category, defined by language.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'research_projectcategory'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class ProjectResearch(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project research type, defined by language.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'research_projectresearch'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class ProjectPartnerFunction(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project partner function, defined by language.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'research_projectpartnerfunction'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class ProjectStudy(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project study, defined by language.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'research_projectstudy'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class ProjectEvent(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project event, defined by language.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'research_projectevent'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class ProjectGrant(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project grant, defined by language.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'research_projectgrant'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class ProjectStatus(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of project status.
    '''
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'research_projectstatus'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


class Project(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project function, defined by language.
    '''
    organization = models.ForeignKey(
        'campusonline.Organization',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        'ProjectCategory',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    short = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    title = HStoreField()
    partner_function = models.ForeignKey(
        'ProjectPartnerFunction',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    manager = models.ForeignKey(
        'campusonline.Person',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    contact = models.ForeignKey(
        'campusonline.Person',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    status = models.ForeignKey(
        'ProjectStatus',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    url = models.URLField(
        blank=True,
        null=True
    )
    abstract = HStoreField()
    begin_planned = models.DateTimeField(
        blank=True,
        null=True
    )
    begin_effective = models.DateTimeField(
        blank=True,
        null=True
    )
    end_planned = models.DateTimeField(
        blank=True,
        null=True
    )
    end_effective = models.DateTimeField(
        blank=True,
        null=True
    )
    grant = models.ForeignKey(
        'ProjectGrant',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    research = models.ForeignKey(
        'ProjectResearch',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    event = models.ForeignKey(
        'ProjectEvent',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    study = models.ForeignKey(
        'ProjectStudy',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    funders = models.ManyToManyField(
        'Funder',
        db_table='research_project_funder',
        db_constraint=False,
        related_name='projects'
    )

    class Meta:
        managed = False
        db_table = 'research_project'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.title.get('de')


class PublicationCategory(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of category, defined by language.
    '''
    name = HStoreField()

    class Meta:
        managed = False
        db_table = 'research_publicationcategory'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get('de')


class PublicationDocument(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of publication document, defined by language.
    '''
    name = HStoreField()

    class Meta:
        managed = False
        db_table = 'research_publicationdocument'

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
        'PublicationCategory',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    document = models.ForeignKey(
        'PublicationDocument',
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
    @memoize(timeout=3600)
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
