# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-24 13:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('key', models.CharField(max_length=30, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(30)])),
                ('name', models.CharField(max_length=256)),
                ('enabled', models.BooleanField(default=False)),
                ('secret', models.CharField(max_length=256)),
                ('rsa', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('nonce', models.CharField(max_length=40)),
                ('token', models.CharField(blank=True, max_length=30, null=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lti.Consumer')),
            ],
        ),
        migrations.AddIndex(
            model_name='history',
            index=models.Index(fields=['consumer', 'timestamp', 'nonce', 'token'], name='lti_history_consume_d363b2_idx'),
        ),
    ]
