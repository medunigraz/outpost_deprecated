# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 08:15
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    forward = [
        '''
        CREATE SCHEMA IF NOT EXISTS typo3;
        ''',
        '''
        CREATE FOREIGN TABLE "typo3"."language" (
            uid integer,
            tstamp integer,
            hidden integer,
            title varchar,
            flag varchar,
            language_isocode varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'sys_language',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('typo3')),
        '''
        CREATE FOREIGN TABLE "typo3"."category" (
            uid integer,
            tstamp integer,
            crdate integer,
            deleted integer,
            hidden integer,
            starttime integer,
            endtime integer,
            sys_language_uid integer,
            title text,
            description text,
            parent integer,
            items integer,
            images integer,
            shortcut integer,
            calendar_id integer,
            tx_odsosm_marker integer
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'sys_category',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('typo3')),
        '''
        CREATE FOREIGN TABLE "typo3"."calendar" (
            uid integer,
            tstamp integer,
            crdate integer,
            deleted integer,
            hidden integer,
            starttime integer,
            endtime integer,
            title text,
            type integer,
            ext_url varchar,
            sys_language_uid integer
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'tx_cal_calendar',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('typo3')),
        '''
        CREATE FOREIGN TABLE "typo3"."event" (
            uid integer,
            tstamp integer,
            crdate integer,
            deleted integer,
            hidden integer,
            starttime integer,
            endtime integer,
            start_date varchar,
            end_date varchar,
            start_time integer,
            end_time integer,
            allday integer,
            timezone varchar,
            title text,
            calendar_id integer,
            category_id integer,
            organizer varchar,
            location text,
            teaser text,
            description text,
            sys_language_uid integer,
            tx_mugcal_register integer,
            tx_mugcal_registration_end integer,
            tx_mugcal_attendingfees integer,
            tx_mugcal_www varchar,
            tx_mugcal_dfppoints integer,
            tx_mugcal_contact varchar,
            tx_mugcal_contact_email varchar,
            tx_mugcal_target integer
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'tx_cal_event',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('typo3')),
        '''
        CREATE FOREIGN TABLE "typo3"."news" (
            uid integer,
            pid integer,
            tstamp integer,
            crdate integer,
            sys_language_uid integer,
            deleted integer,
            hidden integer,
            starttime integer,
            endtime integer,
            sorting integer,
            title text,
            teaser text,
            bodytext text,
            datetime integer,
            archive integer,
            author text,
            author_email text,
            categories integer,
            related integer,
            related_from integer,
            related_files text,
            related_links text,
            type varchar,
            keywords text,
            tags integer,
            media text,
            internalurl text,
            externalurl text,
            istopnews integer,
            content_elements text,
            path_segment text,
            alternative_title text,
            description text,
            fal_related_files integer,
            fal_media integer
        )
        SERVER sqlalchemy
        OPTIONS (
            tablename 'tx_news_domain_model_news',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('typo3')),
        '''
        CREATE VIEW "public"."typo3_language" AS SELECT
            uid AS id,
            title,
            flag,
            language_isocode AS isocode
        FROM "typo3"."language"
        WHERE
            hidden = 0;
        ''',
        '''
        CREATE VIEW "public"."typo3_category" AS SELECT
            uid AS id,
            CASE WHEN
                sys_language_uid > 0
            THEN
                sys_language_uid
            ELSE
                NULL
            END AS language_id,
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
            title,
            description,
            parent,
            tx_odsosm_marker AS marker
        FROM "typo3"."category"
        WHERE
            deleted = 0 AND
            hidden = 0;
        ''',
        '''
        CREATE VIEW "public"."typo3_calendar" AS SELECT
            uid AS id,
            title,
            CASE WHEN
                sys_language_uid > 0
            THEN
                sys_language_uid
            ELSE
                NULL
            END AS language_id
        FROM "typo3"."calendar"
        WHERE
            type = 0 AND
            deleted = 0 AND
            hidden = 0;
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
    reverse = [
        '''
        DROP VIEW IF EXISTS "public"."typo3_news";
        ''',
        '''
        DROP VIEW IF EXISTS "public"."typo3_event";
        ''',
        '''
        DROP VIEW IF EXISTS "public"."typo3_calendar";
        ''',
        '''
        DROP VIEW IF EXISTS "public"."typo3_category";
        ''',
        '''
        DROP VIEW IF EXISTS "public"."typo3_language";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "typo3"."language";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "typo3"."category";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "typo3"."event";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "typo3"."calendar";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "typo3"."news";
        ''',
    ]

    dependencies = [
        ('base', '0005_html_unescape'),
    ]

    operations = [
        migrations.RunSQL(
            forward,
            reverse
        )
    ]
