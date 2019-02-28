# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-02-26 08:59
from __future__ import unicode_literals

from django.db import migrations, models
import outpost.django.base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_auto_20190225_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='behaviour',
            field=outpost.django.base.fields.ChoiceArrayField(base_field=models.CharField(choices=[('outpost.django.attendance.plugins.DebugTerminalBehaviour', 'Debugger'), ('outpost.django.attendance.plugins.StatisticsTerminalBehaviour', 'Statistics'), ('outpost.django.attendance.plugins.CampusOnlineTerminalBehaviour', 'CAMPUSonline')], max_length=256), default=list, size=None),
        ),
    ]