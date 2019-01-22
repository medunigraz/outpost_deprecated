# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-22 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('typo3', '0022_sources'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('private', models.BooleanField()),
            ],
            options={
                'db_table': 'typo3_source',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='djangosource',
            name='id',
            field=models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, related_name='+', serialize=False, to='typo3.Source'),
        ),
    ]
