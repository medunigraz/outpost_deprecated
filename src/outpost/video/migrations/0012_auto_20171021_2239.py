# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 20:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import outpost.base.utils


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0011_auto_20170908_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordingAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('data', models.FileField(upload_to=outpost.base.utils.Uuid4Upload)),
                ('mimetype', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='recorder',
            options={'ordering': ('name', 'hostname'), 'permissions': (('view_recorder', 'View Recorder'),)},
        ),
        migrations.AlterModelOptions(
            name='recording',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='recordingasset',
            name='recording',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.Recording'),
        ),
    ]
