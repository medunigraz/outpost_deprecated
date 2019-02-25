# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-14 19:59
from __future__ import unicode_literals

from django.db import migrations, models
from ...base.fields import ChoiceArrayField


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_auto_20171002_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='behaviour',
            field=ChoiceArrayField(base_field=models.CharField(max_length=256), default=list, size=None),
        ),
    ]