import requests
from django.conf import settings
from django.contrib.gis.db import models
from memoize import memoize
from purl import URL


class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    flag = models.CharField(max_length=2, blank=True, null=True)
    isocode = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_language'

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.title


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
        ordering = (
            'start',
            'end',
        )

    @memoize(timeout=3600)
    def url(self):
        url = URL(settings.OUTPOST['typo3_api'])
        url = url.query_param('tx_mugapi_endpoint[recordType]', 'Event')
        url = url.query_param('tx_mugapi_endpoint[recordUid]', self.pk)
        url = url.query_param('tx_mugapi_endpoint[redirect]', 1)
        r = requests.get(url.as_string(), allow_redirects=False)
        if r.status_code != 302:
            return None
        realurl = URL(r.headers['location'])
        realurl = realurl.fragment('sl-content')
        return realurl.as_string()

    def __str__(self):
        return self.title

    def __repr__(self):
        return '{s.__class__.__name__}({s.pk})'.format(s=self)


class News(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.IntegerField(blank=True, null=True)
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    datetime = models.DateTimeField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    teaser = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    tags = models.IntegerField(blank=True, null=True)
    topnews = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'typo3_news'
        ordering = (
            '-datetime',
        )

    @memoize(timeout=3600)
    def url(self):
        url = URL(settings.OUTPOST['typo3_api'])
        url = url.query_param('tx_mugapi_endpoint[recordType]', 'News')
        url = url.query_param('tx_mugapi_endpoint[recordUid]', self.pk)
        url = url.query_param('tx_mugapi_endpoint[redirect]', 1)
        url = url.fragment('sl-content')
        r = requests.get(url.as_string(), allow_redirects=False)
        if r.status_code != 302:
            return None
        realurl = URL(r.headers['location'])
        realurl = realurl.fragment('sl-content')
        return realurl.as_string()

    def __str__(self):
        return self.title

    def __repr__(self):
        return '{s.__class__.__name__}({s.pk})'.format(s=self)
