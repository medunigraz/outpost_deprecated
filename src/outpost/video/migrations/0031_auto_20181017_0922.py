# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-17 07:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0030_auto_20180628_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broadcast',
            name='stream',
        ),
        migrations.RemoveField(
            model_name='dashaudio',
            name='publishmedia_ptr',
        ),
        migrations.RemoveField(
            model_name='dashpublish',
            name='audio',
        ),
        migrations.RemoveField(
            model_name='dashpublish',
            name='presenter',
        ),
        migrations.RemoveField(
            model_name='dashpublish',
            name='publish_ptr',
        ),
        migrations.RemoveField(
            model_name='dashpublish',
            name='slides',
        ),
        migrations.RemoveField(
            model_name='dashvideo',
            name='publishmedia_ptr',
        ),
        migrations.RemoveField(
            model_name='dashvideovariant',
            name='video',
        ),
        migrations.RemoveField(
            model_name='event',
            name='license',
        ),
        migrations.RemoveField(
            model_name='event',
            name='room',
        ),
        migrations.RemoveField(
            model_name='event',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='eventaudio',
            name='eventmedia_ptr',
        ),
        migrations.RemoveField(
            model_name='eventmedia',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventmedia',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='eventvideo',
            name='eventmedia_ptr',
        ),
        migrations.RemoveField(
            model_name='publish',
            name='event',
        ),
        migrations.RemoveField(
            model_name='publish',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='publishmedia',
            name='eventmedia',
        ),
        migrations.RemoveField(
            model_name='publishmedia',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='publishmediascene',
            name='media',
        ),
        migrations.RemoveField(
            model_name='stream',
            name='active',
        ),
        migrations.RemoveField(
            model_name='token',
            name='stream',
        ),
        migrations.DeleteModel(
            name='Broadcast',
        ),
        migrations.DeleteModel(
            name='DASHAudio',
        ),
        migrations.DeleteModel(
            name='DASHPublish',
        ),
        migrations.DeleteModel(
            name='DASHVideo',
        ),
        migrations.DeleteModel(
            name='DASHVideoVariant',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='EventAudio',
        ),
        migrations.DeleteModel(
            name='EventMedia',
        ),
        migrations.DeleteModel(
            name='EventVideo',
        ),
        migrations.DeleteModel(
            name='Publish',
        ),
        migrations.DeleteModel(
            name='PublishMedia',
        ),
        migrations.DeleteModel(
            name='PublishMediaScene',
        ),
        migrations.DeleteModel(
            name='Stream',
        ),
        migrations.DeleteModel(
            name='Token',
        ),
    ]
