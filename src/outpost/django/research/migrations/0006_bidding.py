# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-01 09:47
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0005_classification_education_expertise_knowledge_program_publicationauthorship_publicationorganization'),
    ]

    ops = [
        (
            '''
            CREATE FOREIGN TABLE "research"."ausschreibung" (
                AUSSCHREIBUNG_ID numeric,
                AUSSCHREIBUNG_TITEL varchar,
                KURZINFO varchar,
                LANGINFO varchar,
                EINREICHMODUS varchar,
                INFO_WEBSITE varchar,
                LAUFEND_JA_NEIN varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'AUSSCHREIBUNG',
                db_url '{}'
            );
            '''.format(settings.MULTICORN.get('research')),
            '''
            DROP FOREIGN TABLE IF EXISTS "research"."ausschreibung";
            ''',
        ),
        (
            '''
            CREATE FOREIGN TABLE "research"."ausschreibung_deadline" (
                DEADLINE_ID numeric,
                AUSSCHREIBUNG_ID numeric,
                DEADLINE timestamp,
                UHRZEIT varchar,
                ANMERKUNG_DEADLINE varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'AUSSCHREIBUNG_DEADLINE',
                db_url '{}'
            );
            '''.format(settings.MULTICORN.get('research')),
            '''
            DROP FOREIGN TABLE IF EXISTS "research"."ausschreibung_deadline";
            ''',
        ),
        (
            '''
            CREATE FOREIGN TABLE "research"."ausschreibung_dotierung" (
                DOTIERUNG_ID numeric,
                AUSSCHREIBUNG_ID numeric,
                INFO_DOTIERUNG varchar,
                BETRAG numeric,
                WAEHRUNG varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'AUSSCHREIBUNG_DOTIERUNG',
                db_url '{}'
            );
            '''.format(settings.MULTICORN.get('research')),
            '''
            DROP FOREIGN TABLE IF EXISTS "research"."ausschreibung_dotierung";
            ''',
        ),
        (
            '''
            CREATE FOREIGN TABLE "research"."ausschreibung_geldgeber" (
                AUSSCHREIBUNG_ID numeric,
                GELDGEBER_ID numeric
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'AUSSCHREIBUNG_GELDGEBER',
                db_url '{}'
            );
            '''.format(settings.MULTICORN.get('research')),
            '''
            DROP FOREIGN TABLE IF EXISTS "research"."ausschreibung_geldgeber";
            ''',
        ),
        (
            '''
            CREATE MATERIALIZED VIEW "public"."research_bidding" AS SELECT
                AUSSCHREIBUNG_ID::integer AS id,
                AUSSCHREIBUNG_TITEL AS title,
                KURZINFO AS short,
                LANGINFO AS description,
                EINREICHMODUS as mode,
                INFO_WEBSITE AS url,
                (LOWER(LAUFEND_JA_NEIN) = 'ja')::boolean AS running
            FROM
                "research"."ausschreibung"
            ''',
            '''
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_bidding";
            ''',
        ),
        (
            '''
            CREATE MATERIALIZED VIEW "public"."research_biddingdeadline" AS SELECT
                DEADLINE_ID::integer AS id,
                AUSSCHREIBUNG_ID::integer AS bidding_id,
                DEADLINE::timestamptz AS deadline,
                UHRZEIT AS time,
                ANMERKUNG_DEADLINE AS comment
            FROM
                "research"."ausschreibung_deadline"
            ''',
            '''
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_biddingdeadline";
            ''',
        ),
        (
            '''
            CREATE MATERIALIZED VIEW "public"."research_biddingendowment" AS SELECT
                DOTIERUNG_ID::integer AS id,
                AUSSCHREIBUNG_ID::integer AS bidding_id,
                INFO_DOTIERUNG AS information,
                BETRAG::money AS amount,
                WAEHRUNG AS currency
            FROM
                "research"."ausschreibung_dotierung"
            ''',
            '''
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_biddingendowment";
            ''',
        ),
        (
            '''
            CREATE MATERIALIZED VIEW "public"."research_bidding_funder" AS SELECT
                AUSSCHREIBUNG_ID::integer AS bidding_id,
                GELDGEBER_ID::integer AS funder_id
            FROM
                "research"."ausschreibung_geldgeber"
            ''',
            '''
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_bidding_funder";
            ''',
        ),
        (
            '''
            CREATE UNIQUE INDEX research_bidding_id_idx ON "public"."research_bidding" ("id");
            ''',
            '''
            DROP INDEX IF EXISTS research_bidding_id_idx;
            ''',
        ),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)]
        )
    ]
