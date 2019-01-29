# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-29 12:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salt', '0002_auto_20181030_1239'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('key', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salt.User')),
            ],
        ),
    ]
