# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-17 14:42
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
                ('iso', models.CharField(blank=True, max_length=2, null=True)),
            ],
            options={
                'db_table': 'research_country',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Funder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
                ('street', models.CharField(blank=True, max_length=256, null=True)),
                ('city', models.CharField(blank=True, max_length=256, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=32, null=True)),
                ('url', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'research_funder',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FunderCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
                ('short', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'research_fundercategory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
                ('iso', models.CharField(blank=True, max_length=2, null=True)),
            ],
            options={
                'db_table': 'research_language',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(blank=True, max_length=256, null=True)),
                ('title', django.contrib.postgres.fields.hstore.HStoreField()),
                ('url', models.URLField(blank=True, null=True)),
                ('abstract', django.contrib.postgres.fields.hstore.HStoreField()),
                ('begin_planned', models.DateTimeField(blank=True, null=True)),
                ('begin_effective', models.DateTimeField(blank=True, null=True)),
                ('end_planned', models.DateTimeField(blank=True, null=True)),
                ('end_effective', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'research_project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'research_projectcategory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'research_projectevent',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectGrant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'research_projectgrant',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectPartnerFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'research_projectpartnerfunction',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectResearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'research_projectresearch',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'research_projectstatus',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectStudy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'research_projectstudy',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('authors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), size=None)),
                ('year', models.PositiveSmallIntegerField()),
                ('source', models.TextField()),
                ('sci', models.CharField(blank=True, max_length=128, null=True)),
                ('pubmed', models.CharField(blank=True, max_length=128, null=True)),
                ('doi', models.CharField(blank=True, max_length=128, null=True)),
                ('pmc', models.CharField(blank=True, max_length=128, null=True)),
                ('abstract_bytes', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'research_publication',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PublicationCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'research_publicationcategory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PublicationDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'research_publicationdocument',
                'managed': False,
            },
        ),
    ]