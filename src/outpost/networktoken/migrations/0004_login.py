# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-22 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networktoken', '0003_radius_schema'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=256)),
                ('password', models.CharField(default='', max_length=256)),
                ('response', models.CharField(default='', max_length=256)),
                ('created', models.DateTimeField()),
            ],
        ),
    ]
