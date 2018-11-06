# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 08:21
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('typo3', '0003_auto_20170818_1538'),
    ]

    forward = [
        '''
        DROP VIEW IF EXISTS "public"."typo3_event";
        ''',
        '''
        DROP VIEW IF EXISTS "public"."typo3_news";
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."typo3_event" AS SELECT
            uid AS id,
            pid AS page,
            to_date(start_date, 'YYYYMMDD') + CASE
                allday
            WHEN
                1
            THEN
                interval '0 hours'
            ELSE
                start_time * interval '1 seconds'
            END AS "start",
            to_date(end_date, 'YYYYMMDD') + CASE
                allday
            WHEN
                1
            THEN
                interval '24 hours'
            ELSE
                end_time * interval '1 seconds'
            END AS "end",
            allday::boolean AS allday,
            html_unescape(title) AS title,
            calendar_id,
            CASE WHEN
                category_id > 0
            THEN
                category_id
            ELSE
                NULL
            END AS category_id,
            organizer,
            location,
            html_unescape(teaser) AS teaser,
            html_unescape(description) AS description,
            CASE WHEN
                sys_language_uid > 0
            THEN
                sys_language_uid
            ELSE
                NULL
            END AS language_id,
            tx_mugcal_register::boolean AS register,
            CASE WHEN
                tx_mugcal_registration_end > 0
            THEN
                to_timestamp(tx_mugcal_registration_end)
            ELSE
                NULL
            END AS registration_end,
            tx_mugcal_attendingfees::boolean AS attending_fees,
            tx_mugcal_www AS url,
            tx_mugcal_dfppoints AS dfp_points,
            tx_mugcal_contact AS contact,
            tx_mugcal_contact_email AS email,
            to_timestamp(tstamp) AS last_modified
        FROM "typo3"."event"
        WHERE
            start_date != '0' AND
            end_date != '0' AND
            (starttime = 0 OR to_timestamp(starttime) > NOW()) AND
            to_date(end_date, 'YYYYMMDD') + CASE
                allday
            WHEN
                1
            THEN
                interval '24 hours'
            ELSE
                end_time * interval '1 seconds'
            END > NOW() AND
            deleted = 0 AND
            hidden = 0
        WITH DATA;
        '''.format(typo3_fileadmin=settings.OUTPOST.get('typo3_fileadmin')),
        '''
        CREATE MATERIALIZED VIEW "public"."typo3_news" AS SELECT
            uid AS id,
            pid AS page,
            CASE WHEN
                sys_language_uid > 0
            THEN
                sys_language_uid
            ELSE
                NULL
            END AS language_id,
            CASE
                datetime
            WHEN
                0
            THEN
                NULL
            ELSE
                to_timestamp(datetime)
            END AS datetime,
            html_unescape(title) AS title,
            html_unescape(teaser) AS teaser,
            html_unescape(bodytext) AS body,
            CASE
                starttime
            WHEN
                0
            THEN
                NULL
            ELSE
                to_timestamp(starttime)
            END AS start,
            CASE
                endtime
            WHEN
                0
            THEN
                NULL
            ELSE
                to_timestamp(endtime)
            END AS end,
            author,
            author_email AS email,
            keywords,
            tags,
            istopnews = 1 AS topnews,
            to_timestamp(tstamp) AS last_modified
        FROM "typo3"."news"
        WHERE
            (starttime = 0 OR to_timestamp(starttime) < NOW()) AND
            (endtime = 0 OR to_timestamp(endtime) > NOW()) AND
            deleted = 0 AND
            hidden = 0
        WITH DATA;
        '''.format(typo3_fileadmin=settings.OUTPOST.get('typo3_fileadmin')),
    ]

    reverse = [
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_event";
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_news";
        ''',
        '''
        CREATE VIEW "public"."typo3_event" AS SELECT
            uid AS id,
            to_date(start_date, 'YYYYMMDD') + CASE
                allday
            WHEN
                1
            THEN
                interval '0 hours'
            ELSE
                start_time * interval '1 seconds'
            END AS "start",
            to_date(end_date, 'YYYYMMDD') + CASE
                allday
            WHEN
                1
            THEN
                interval '24 hours'
            ELSE
                end_time * interval '1 seconds'
            END AS "end",
            allday::boolean AS allday,
            title,
            calendar_id,
            CASE WHEN
                category_id > 0
            THEN
                category_id
            ELSE
                NULL
            END AS category_id,
            organizer,
            location,
            teaser,
            description,
            CASE WHEN
                sys_language_uid > 0
            THEN
                sys_language_uid
            ELSE
                NULL
            END AS language_id,
            tx_mugcal_register::boolean AS register,
            CASE WHEN
                tx_mugcal_registration_end > 0
            THEN
                to_timestamp(tx_mugcal_registration_end)
            ELSE
                NULL
            END AS registration_end,
            tx_mugcal_attendingfees::boolean AS attending_fees,
            tx_mugcal_www AS url,
            tx_mugcal_dfppoints AS dfp_points,
            tx_mugcal_contact AS contact,
            tx_mugcal_contact_email AS email,
            tx_mugcal_target AS target
        FROM "typo3"."event"
        WHERE
            start_date != '0' AND
            end_date != '0' AND
            (starttime = 0 OR to_timestamp(starttime) > NOW()) AND
            to_date(end_date, 'YYYYMMDD') + CASE
                allday
            WHEN
                1
            THEN
                interval '24 hours'
            ELSE
                end_time * interval '1 seconds'
            END > NOW() AND
            deleted = 0 AND
            hidden = 0;
        ''',
        '''
        CREATE VIEW "public"."typo3_news" AS SELECT
            uid AS id,
            pid AS page,
            CASE WHEN
                sys_language_uid > 0
            THEN
                sys_language_uid
            ELSE
                NULL
            END AS language_id,
            CASE
                datetime
            WHEN
                0
            THEN
                NULL
            ELSE
                to_timestamp(datetime)
            END AS datetime,
            title,
            teaser,
            bodytext AS body,
            author,
            author_email AS email,
            keywords,
            tags,
            istopnews = 1 AS topnews
        FROM "typo3"."news"
        WHERE
            (starttime = 0 OR to_timestamp(starttime) < NOW()) AND
            (endtime = 0 OR to_timestamp(endtime) > NOW()) AND
            deleted = 0 AND
            hidden = 0;
        ''',
    ]

    operations = [
        migrations.RunSQL(
            forward,
            reverse
        )
    ]
