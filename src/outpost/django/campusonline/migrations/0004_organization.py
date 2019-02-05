# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-03 06:11
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    forward = [
        """
        CREATE FOREIGN TABLE "campusonline"."organisationen" (
            NR numeric,
            ORG_NAME varchar,
            ADRESSE varchar,
            EMAIL_ADRESSE varchar,
            TELEFON_NUMMER varchar,
            WWW_HOMEPAGE varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'ORGANISATIONEN_V',
            db_url '{}'
        );
        """.format(settings.MULTICORN.get('campusonline')),
        """
        CREATE FOREIGN TABLE "campusonline"."personen" (
            PERS_NR numeric,
            PERS_VORNAME varchar,
            PERS_FAMNAM varchar,
            PERS_TITEL varchar,
            RAUM_NR numeric
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'PERSON_V',
            db_url '{}'
        );
        """.format(settings.MULTICORN.get('campusonline')),
        """
        CREATE MATERIALIZED VIEW "public"."campusonline_organization" AS SELECT
            nr::integer AS id,
            org_name AS name,
            adresse AS address,
            email_adresse AS email,
            telefon_nummer AS phone,
            www_homepage AS url
        FROM "campusonline"."organisationen"
        WITH DATA;
        """,
        """
        CREATE MATERIALIZED VIEW "public"."campusonline_person" AS SELECT
            pers_nr ::integer AS id,
            pers_vorname AS first_name,
            pers_famnam AS last_name,
            pers_titel AS title,
            raum_nr ::integer AS room_id
        FROM "campusonline"."personen"
        WITH DATA;
        """,
    ]
    reverse = [
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_person";
        """,
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_organization";
        """,
        """
        DROP FOREIGN TABLE IF EXISTS "campusonline"."personen";
        """,
        """
        DROP FOREIGN TABLE IF EXISTS "campusonline"."organisationen";
        """,
    ]

    dependencies = [
        ('campusonline', '0003_materialized'),
    ]

    operations = [
        migrations.RunSQL(
            forward,
            reverse
        )
    ]