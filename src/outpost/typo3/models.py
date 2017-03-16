from django.contrib.gis.db import models


class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    flag = models.CharField(max_length=2, blank=True, null=True)
    isocode = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_language'


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    marker = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_category'


class Calendar(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    class Meta:
        managed = False
        db_table = 'typo3_calendar'


class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    allday = models.BooleanField()
    title = models.TextField(blank=True, null=True)
    calendar = models.ForeignKey(
        'Calendar',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    category = models.ForeignKey(
        'Category',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    organizer = models.CharField(max_length=256, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    teaser = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    register = models.BooleanField()
    registration_end = models.DateTimeField(blank=True, null=True)
    attending_fees = models.BooleanField()
    url = models.CharField(max_length=512, blank=True, null=True)
    dfp_points = models.IntegerField(blank=True, null=True)
    contact = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    target = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_event'


class News(models.Model):
    id = models.IntegerField(primary_key=True)
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    teaser = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    tags = models.IntegerField(blank=True, null=True)
    topnews = models.BooleanField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_news'
