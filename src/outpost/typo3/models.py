from django.contrib.gis.db import models


class News(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(blank=True, null=True)
    language_id = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    teaser = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    tags = models.IntegerField(blank=True, null=True)
    topnews = models.NullBooleanField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_news'


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(blank=True, null=True)
    language_id = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    calendar_id = models.IntegerField(blank=True, null=True)
    marker = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_categories'
