# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-28 13:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campusonline', '0037_auto_20190128_1104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bulletinpage',
            old_name='number',
            new_name='index',
        ),
    ]