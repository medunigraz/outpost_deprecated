import logging

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class DoctoralSchool(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of doctoral school.

    ### `emails` (`string[]`)
    Contact emails.
    '''
    id = models.IntegerField(
        primary_key=True
    )
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    emails = ArrayField(
        models.EmailField(
            blank=True,
            null=True
        )
    )

    class Meta:
        managed = False
        db_table = 'thesis_doctoralschool'

    def __str__(self):
        return self.name


class Discipline(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of discipline.

    ### `number` (`string`)
    Number of discipline.

    ### `thesistype` (`string`)
    Type of thesis conducted. Possible values are:

     * ``
    '''
    id = models.IntegerField(
        primary_key=True
    )
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    number = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    thesistype = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'thesis_discipline'

    def __str__(self):
        return self.name


class Thesis(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `topic` (`string`)
    Topic of thesis.

    ### `created` (`datetime`)
    Date and time when thesis proposal was created.

    ### `description` (`string`)
    Full description of thesis.

    ### `prerequisites` (`string`)
    Prerequisites for thesis.

    ### `processstart` (`datetime`)
    Start of thesis process.

    ### `goals` (`string`)
    Goals for thesis.

    ### `hypothesis` (`string`)
    Hypothesis of thesis.

    ### `methods` (`string`)
    Methods used in thesis.

    ### `schedule` (`string`)
    Schedule for thesis.

    ### `milestones` (`string[]`)
    List of milestones for thesis. Order is from earliest to latest milestone.

    ### `discipline` (`integer` or `Object`)
    Foreign key to [Thesis discipline](../discipline) that thesis belongs to.

    ### `doctoralschool` (`integer` or `Object`)
    Foreign key to [Thesis doctoral school](../doctoralschool) that thesis belongs to.

    ### `editors` (`integer[]` or `Object[]`)
    List of foreign keys to [CAMPUSonline persons](../../campusonline/person) that are editors to this thesis.
    '''
    id = models.IntegerField(
        primary_key=True
    )
    topic = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    prerequisites = models.TextField(
        blank=True,
        null=True
    )
    processstart = models.DateTimeField(
        blank=True,
        null=True
    )
    goals = models.TextField(
        blank=True,
        null=True
    )
    hypothesis = models.TextField(
        blank=True,
        null=True
    )
    methods = models.TextField(
        blank=True,
        null=True
    )
    schedule = models.TextField(
        blank=True,
        null=True
    )
    milestones = ArrayField(
        models.TextField(
            blank=True,
            null=True
        )
    )
    discipline = models.ForeignKey(
        'Discipline',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='thesis'
    )
    doctoralschool = models.ForeignKey(
        'DoctoralSchool',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='thesis'
    )
    editors = models.ManyToManyField(
        'campusonline.Person',
        db_table='thesis_editor',
        db_constraint=False,
        related_name='thesis'
    )

    class Meta:
        managed = False
        db_table = 'thesis_thesis'
        permissions = (
            ('view_thesis', _('View thesis')),
        )

    def __str__(self):
        return self.topic
