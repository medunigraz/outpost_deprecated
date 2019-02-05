# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-22 13:27
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('typo3', '0019_auto_20181211_0939'),
    ]

    forward = [
        '''
        CREATE FOREIGN TABLE "typo3"."pages" (
            uid int4,
            pid int4,
            tstamp int4,
            crdate int4,
            deleted int4,
            hidden int4,
            title text
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'pages',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('typo3')),
        '''
        CREATE MATERIALIZED VIEW "typo3"."source_typo3" AS
        SELECT
            p.uid AS id,
            p.title
        FROM "typo3"."pages" AS p
        WHERE
        p.deleted = 0 AND
        p.hidden = 0 AND
        (
            (SELECT COUNT(1) FROM "typo3"."news" AS n WHERE n.pid = p.uid) > 0
            OR
            (SELECT COUNT(1) FROM "typo3"."event" AS e WHERE e.pid = p.uid) > 0
        )
        ''',
        #'''
        #CREATE VIEW "public"."typo3_source" AS
        #SELECT
        #s_t.id AS id,
        #s_t.title AS title,
        #COALESCE(s_d.private, FALSE) AS private
        #FROM "typo3"."source_typo3" AS s_t
        #LEFT OUTER JOIN
        #    "typo3"."source_django" AS s_d
        #    ON s_t.id = s_d.id
        #''',
    ]

    reverse = [
        '''
        DROP MATERIALIZED VIEW IF EXISTS "typo3"."source_typo3";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "typo3"."pages";
        ''',
    ]

    operations = [
        migrations.RunSQL(
            forward,
            reverse
        )
    ]