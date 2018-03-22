# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-22 16:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('networktoken', '0005_protocol_view'),
    ]

    forward = [
        f'''
        GRANT USAGE ON SCHEMA radius TO {settings.RADIUS_USER};
        ''',
        f'''
        GRANT SELECT ON radius.token TO {settings.RADIUS_USER};
        ''',
        f'''
        GRANT SELECT ON radius.reply TO {settings.RADIUS_USER};
        ''',
        f'''
        GRANT INSERT ON radius.protocol TO {settings.RADIUS_USER};
        ''',
        f'''
        GRANT USAGE, SELECT ON SEQUENCE public.networktoken_login_id_seq TO {settings.RADIUS_USER};
        ''',
    ]

    reverse = [
    ]

    operations = [
        migrations.RunSQL(
            forward,
            reverse
        )
    ]
