# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-28 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campusonline', '0024_pers_org_funk'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonOrganizationFunction',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'campusonline_personorganizationfunction',
                'ordering': ('id',),
                'managed': False,
            },
        ),
    ]