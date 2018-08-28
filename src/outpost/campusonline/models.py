from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel
from treebeard.al_tree import AL_Node


class RoomCategory(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'campusonline_room_category'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    building = models.ForeignKey(
        'Building',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    floor = models.ForeignKey(
        'Floor',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    name_short = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    name_full = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    area = models.DecimalField(
        max_digits=65535,
        decimal_places=1,
        blank=True,
        null=True
    )
    height = models.DecimalField(
        max_digits=65535,
        decimal_places=1,
        blank=True,
        null=True
    )
    organization = models.ForeignKey(
        'Organization',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    category = models.ForeignKey(
        'RoomCategory',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    class Meta:
        managed = False
        db_table = 'campusonline_room'
        ordering = (
            'name_full',
            'title',
        )

    def __str__(self):
        return '{s.name_full}: {s.title}'.format(s=self)


class Floor(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    short = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'campusonline_floor'
        ordering = (
            'name',
        )

    def __str__(self):
        return '{s.name} ({s.short})'.format(s=self)


class Building(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    short = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'campusonline_building'
        ordering = (
            'name',
        )

    def __str__(self):
        return '{s.name} ({s.short})'.format(s=self)


class Function(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    category = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    persons = models.ManyToManyField(
        'Person',
        through='PersonOrganizationFunction'
    )

    class Meta:
        managed = False
        db_table = 'campusonline_function'
        ordering = (
            'name',
            'category',
        )

    def __str__(s):
        return f'{s.name} ({s.category})'


class Organization(AL_Node):
    id = models.IntegerField(
        primary_key=True
    )
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    short = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    parent = models.ForeignKey(
        'self',
        models.SET_NULL,
        related_name='children_set',
        db_constraint=False,
        db_index=False,
        null=True,
        blank=True
    )
    sib_order = models.PositiveIntegerField()
    category = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    address = models.TextField(
        blank=True,
        null=True
    )
    email = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    url = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'campusonline_organization'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name


class Person(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    first_name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    room = models.ForeignKey(
        'Room',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    sex = models.CharField(
        max_length=1,
        blank=True,
        null=True
    )
    username = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    consultation = models.TextField(
        blank=True,
        null=True
    )
    appendix = models.TextField(
        blank=True,
        null=True
    )
    avatar = models.URLField(
        blank=True,
        null=True
    )
    functions = models.ManyToManyField(
        'Function',
        through='PersonOrganizationFunction'
    )

    class Meta:
        managed = False
        db_table = 'campusonline_person'
        ordering = (
            'last_name',
            'first_name',
        )

    def __str__(self):
        return '{s.last_name}, {s.first_name}'.format(s=self)


class PersonOrganizationFunction(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=128
    )
    person = models.ForeignKey(
        'Person',
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name='+'
    )
    organization = models.ForeignKey(
        'Organization',
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name='+'
    )
    function = models.ForeignKey(
        'function',
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name='+'
    )

    class Meta:
        managed = False
        db_table = 'campusonline_personorganizationfunction'
        ordering = (
            'id',
        )

    def __str__(self):
        return '{s.person}, {s.organization}: {s.function}'.format(s=self)


class Student(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    matriculation = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=256
    )
    last_name = models.CharField(
        max_length=256
    )
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    cardid = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'campusonline_student'
        ordering = (
            'last_name',
            'first_name',
        )

    def __str__(self):
        return '{s.last_name}, {s.first_name}'.format(s=self)


class Course(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    name = models.CharField(
        max_length=256
    )
    category = models.CharField(
        max_length=256
    )
    year = models.CharField(
        max_length=256
    )
    semester = models.CharField(
        max_length=256
    )

    class Meta:
        managed = False
        db_table = 'campusonline_course'

    def __str__(self):
        return '{s.name} ({s.semester}:{s.year})'.format(s=self)


class CourseGroup(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    course = models.ForeignKey(
        'Course',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    name = models.CharField(
        max_length=256
    )
    students = models.ManyToManyField(
        'Student'
    )

    class Meta:
        managed = False
        db_table = 'campusonline_coursegroup'

    def __str__(self):
        return '{s.name} ({s.course})'.format(s=self)


class CourseGroupTerm(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=128
    )
    title = models.TextField(
        null=True
    )
    coursegroup = models.ForeignKey(
        'CourseGroup',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    person = models.ForeignKey(
        'Person',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    term = models.IntegerField()
    room = models.ForeignKey(
        'Room',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = 'campusonline_coursegroupterm'
        ordering = (
            'start',
            'end',
        )
        permissions = (
            ('view_coursegroupterm', _('Can view course group term')),
        )

    def __str__(s):
        return f'{s.coursegroup} ({s.person}): {s.room} {s.start}-{s.end}'


class Event(OrderedModel):
    id = models.CharField(
        primary_key=True,
        max_length=32
    )
    course = models.ForeignKey(
        'Course',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    category = models.CharField(
        max_length=256
    )
    title = models.CharField(
        max_length=256
    )
    date = models.DateTimeField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    building = models.ForeignKey(
        'Building',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    room = models.ForeignKey(
        'Room',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    show_end = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'campusonline_event'

    def __str__(self):
        return '{s.category} {s.date}: {s.title} ({s.room})'.format(s=self)


class Bulletin(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    academic_year = models.CharField(
        max_length=256
    )
    issue = models.CharField(
        max_length=256
    )
    published = models.DateTimeField()
    teaser = models.TextField()
    url = models.URLField()

    class Meta:
        managed = False
        db_table = 'campusonline_bulletin'
        ordering = (
            '-published',
        )

    def __str__(s):
        return f'{s.issue} {s.academic_year} ({s.published})'
