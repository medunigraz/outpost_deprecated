# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-07 14:08
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    forward = [
        '''
        CREATE SCHEMA IF NOT EXISTS research;
        ''',
        '''
        CREATE FOREIGN TABLE "research"."forschung_art" (
            FORSCHUNG_ART_ID numeric,
            FORSCHUNG_ART_DE varchar,
            FORSCHUNG_ART_EN varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'FORSCHUNG_ART_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."geldgeber" (
            GELDGEBER_ID numeric,
            GELDGEBER_DE varchar,
            GELDGEBER_EN varchar,
            STRASSE varchar,
            ORT varchar,
            POSTLEITZAHL varchar,
            LAND_ID numeric,
            URL varchar,
            GELDGEBER_TYP_ID numeric
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'GELDGEBER',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."geldgeber_typ" (
            GELDGEBER_TYP_ID numeric,
            GELDGEBER_TYP_DE varchar,
            GELDGEBER_TYP_EN varchar,
            GELDGEBER_TYP_KURZ varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'GELDGEBER_TYP_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."land" (
            LAND_ID numeric,
            LAND_DE varchar,
            LAND_EN varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'LAND_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."org_partner_projektfunktion" (
            ORG_PARTNER_PROJEKTFUNKTION_ID numeric,
            ORG_PARTNER_PROJEKTFUNKTION_DE varchar,
            ORG_PARTNER_PROJEKTFUNKTION_EN varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'ORG_PARTNER_PROJEKTFUNKTION_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."projekt_typ" (
            PROJEKT_TYP_ID numeric,
            PROJEKT_TYP_DE varchar,
            PROJEKT_TYP_EN varchar,
            PROJEKT_TYP_KURZ_DE varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'PROJEKT_TYP_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."projekt" (
            PROJEKT_ID numeric,
            ORGEINHEIT_ID numeric,
            PROJEKT_TYP_ID numeric,
            KURZBEZEICHNUNG varchar,
            PROJEKTTITEL_DE varchar,
            PROJEKTTITEL_EN varchar,
            ORG_PARTNER_PROJEKTFUNKTION_ID numeric,
            PROJEKTLEITER_ID numeric,
            KONTAKTPERSON_ID numeric,
            PROJEKT_STATUS_ID numeric,
            PROJEKT_URL varchar,
            ABSTRACT_DE varchar,
            ABSTRACT_EN varchar,
            PROJEKTBEGINN_GEPLANT timestamp,
            PROJEKTBEGINN_EFFEKTIV timestamp,
            PROJEKTENDE_GEPLANT timestamp,
            PROJEKTENDE_EFFEKTIV timestamp,
            VERGABE_ART_ID numeric,
            FORSCHUNG_ART_ID numeric,
            VERANSTALTUNG_ART_ID numeric,
            STUDIE_ART_ID numeric,
            SPRACHE_ID numeric
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'PROJEKT',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."projekt_geldgeber" (
            PROJEKT_ID numeric,
            GELDGEBER_ID numeric,
            HAUPTGELDGEBER_JA_NEIN varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'PROJEKT_GELDGEBER',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."projekt_status" (
            PROJEKT_STATUS_ID numeric,
            PROJEKT_STATUS varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'PROJEKT_STATUS_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."sprache" (
            SPRACHE_ID numeric,
            SPRACHE_DE varchar,
            SPRACHE_EN varchar,
            SPRACHE_EN_KURZ varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'SPRACHE_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."studie_art" (
            STUDIE_ART_ID numeric,
            STUDIE_ART_DE varchar,
            STUDIE_ART_EN varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'STUDIE_ART_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."veranstaltung_art" (
            VERANSTALTUNG_ART_ID numeric,
            VERANSTALTUNG_ART_DE varchar,
            VERANSTALTUNG_ART_EN varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'VERANSTALTUNG_ART_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."vergabe_art" (
            VERGABE_ART_ID numeric,
            VERGABE_ART_DE varchar,
            VERGABE_ART_EN varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'VERGABE_ART_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."person_publikation" (
            MEDONLINE_PERSON_ID numeric,
            PUBLIKATION_ID numeric
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'PERSON_PUBLIKATION',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."orgeinheit_publikation" (
            PUBLIKATION_ID numeric,
            MEDONLINE_ID numeric
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'ORGEINHEIT_PUBLIKATION',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."publikation_typ" (
            PUBLIKATION_TYP_ID numeric,
            PUBLIKATION_TYP_DE varchar,
            PUBLIKATION_TYP_EN varchar,
            SORTIERUNG_ID numeric
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'PUBLIKATION_TYP_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."publikation_dokumenttyp" (
            PUBLIKATION_DOKUMENTTYP_ID numeric,
            PUBLIKATION_DOKUMENTTYP_DE varchar,
            PUBLIKATION_DOKUMENTTYP_EN varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'PUBLIKATION_DOKUMENTTYP_L',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE FOREIGN TABLE "research"."publikation" (
            PUBLIKATION_ID varchar,
            TITEL varchar,
            AUTOR varchar,
            JAHR numeric,
            QUELLE varchar,
            PUBLIKATION_TYP_ID numeric,
            PUBLIKATION_DOKUMENTTYP_ID numeric,
            SCI_ID varchar,
            PUBMED_ID varchar,
            DOI varchar,
            PMC_ID varchar,
            ABSTRACT bytea
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'PUBLIKATION',
            db_url '{}'
        );
        '''.format(settings.MULTICORN.get('research')),
        '''
        CREATE MATERIALIZED VIEW "public"."research_projectcategory" AS SELECT
            PROJEKT_TYP_ID::integer AS id,
            PROJEKT_TYP_DE AS name,
            PROJEKT_TYP_KURZ_DE AS short
        FROM
            "research"."projekt_typ"
        ''',
        '''
        CREATE UNIQUE INDEX research_projectcategory_id_idx ON "public"."research_projectcategory" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_projectresearch" AS SELECT
            FORSCHUNG_ART_ID::integer AS id,
            FORSCHUNG_ART_DE AS name
        FROM
            "research"."forschung_art"
        ''',
        '''
        CREATE UNIQUE INDEX research_projectresearch_id_idx ON "public"."research_projectresearch" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_funder" AS SELECT
            GELDGEBER_ID::integer AS id,
            GELDGEBER_DE AS name,
            STRASSE AS street,
            ORT AS city,
            POSTLEITZAHL AS zipcode,
            LAND_ID::integer AS country_id,
            URL,
            GELDGEBER_TYP_ID::integer AS category_id
        FROM
            "research"."geldgeber"
        ''',
        '''
        CREATE UNIQUE INDEX research_funder_id_idx ON "public"."research_funder" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_fundercategory" AS SELECT
            GELDGEBER_TYP_ID::integer AS id,
            GELDGEBER_TYP_DE AS name,
            GELDGEBER_TYP_KURZ AS short
        FROM
            "research"."geldgeber_typ"
        ''',
        '''
        CREATE UNIQUE INDEX research_fundercategory_id_idx ON "public"."research_fundercategory" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_country" AS SELECT
            LAND_ID::integer AS id,
            LAND_DE AS name
        FROM
            "research"."land"
        ''',
        '''
        CREATE UNIQUE INDEX research_country_id_idx ON "public"."research_country" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_projectpartnerfunction" AS SELECT
            ORG_PARTNER_PROJEKTFUNKTION_ID::integer AS id,
            ORG_PARTNER_PROJEKTFUNKTION_DE AS name
        FROM
            "research"."org_partner_projektfunktion"
        ''',
        '''
        CREATE UNIQUE INDEX research_projectpartnerfunction_id_idx ON "public"."research_projectpartnerfunction" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_project" AS SELECT
            PROJEKT_ID::integer AS id,
            ORGEINHEIT_ID::integer AS organization_id,
            PROJEKT_TYP_ID::integer AS category_id,
            KURZBEZEICHNUNG AS short,
            hstore(
                ARRAY['de', 'en'],
                ARRAY[PROJEKTTITEL_DE, PROJEKTTITEL_EN]
            ) AS title,
            ORG_PARTNER_PROJEKTFUNKTION_ID::integer AS partner_function_id,
            PROJEKTLEITER_ID::integer AS manager_id,
            KONTAKTPERSON_ID::integer AS contact_id,
            PROJEKT_STATUS_ID::integer AS status_id,
            PROJEKT_URL AS url,
            hstore(
                ARRAY['de', 'en'],
                ARRAY[ABSTRACT_DE, ABSTRACT_EN]
            ) AS abstract,
            PROJEKTBEGINN_GEPLANT::timestamptz AS begin_planned,
            PROJEKTBEGINN_EFFEKTIV::timestamptz AS begin_effective,
            PROJEKTENDE_GEPLANT::timestamptz AS end_planned,
            PROJEKTENDE_EFFEKTIV::timestamptz AS end_effective,
            VERGABE_ART_ID::integer AS grant_id,
            FORSCHUNG_ART_ID::integer AS research_id,
            VERANSTALTUNG_ART_ID::integer AS event_id,
            STUDIE_ART_ID::integer AS study_id,
            SPRACHE_ID::integer AS language_id
        FROM
            research.projekt
        INNER JOIN
            campusonline.personen AS co_p_m
            ON projekt.projektleiter_id::integer = co_p_m.pers_nr::integer
        INNER JOIN
            campusonline.personen AS co_p_c
            ON projekt.kontaktperson_id::integer = co_p_c.pers_nr::integer
        INNER JOIN
            campusonline.organisationen AS co_o
            ON projekt.orgeinheit_id::integer = co_o.nr::integer
        ''',
        '''
        CREATE UNIQUE INDEX research_project_id_idx ON "public"."research_project" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_project_funder" AS SELECT
            PROJEKT_ID::integer AS project_id,
            GELDGEBER_ID::integer AS funder_id,
            CASE lower(HAUPTGELDGEBER_JA_NEIN) WHEN 'ja' THEN TRUE ELSE FALSE END AS primary
        FROM
            "research"."projekt_geldgeber"
        ''',
        '''
        CREATE UNIQUE INDEX research_project_funder_idx ON "public"."research_project_funder" ("project_id", "funder_id");
        ''',
        '''
        CREATE INDEX research_project_funder_project_id_idx ON "public"."research_project_funder" ("project_id");
        ''',
        '''
        CREATE INDEX research_project_funder_funder_id_idx ON "public"."research_project_funder" ("funder_id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_projectstatus" AS SELECT
            PROJEKT_STATUS_ID::integer AS id,
            PROJEKT_STATUS AS name
        FROM
            "research"."projekt_status"
        ''',
        '''
        CREATE UNIQUE INDEX research_projectstatus_id_idx ON "public"."research_projectstatus" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_language" AS SELECT
            SPRACHE_ID::integer AS id,
            SPRACHE_DE AS name,
            SPRACHE_EN_KURZ AS iso
        FROM
            "research"."sprache"
        ''',
        '''
        CREATE UNIQUE INDEX research_language_id_idx ON "public"."research_language" ("id");
        ''',
        '''
        CREATE INDEX research_language_iso_idx ON "public"."research_language" ("iso");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_projectstudy" AS SELECT
            STUDIE_ART_ID::integer AS id,
            STUDIE_ART_DE AS name
        FROM
            "research"."studie_art"
        ''',
        '''
        CREATE UNIQUE INDEX research_projectstudy_id_idx ON "public"."research_projectstudy" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_projectevent" AS SELECT
            VERANSTALTUNG_ART_ID::integer AS id,
            VERANSTALTUNG_ART_DE AS name
        FROM
            "research"."veranstaltung_art"
        ''',
        '''
        CREATE UNIQUE INDEX research_projectevent_id_idx ON "public"."research_projectevent" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_projectgrant" AS SELECT
            VERGABE_ART_ID::integer AS id,
            VERGABE_ART_DE AS name
        FROM
            "research"."vergabe_art"
        ''',
        '''
        CREATE UNIQUE INDEX research_projectgrant_id_idx ON "public"."research_projectgrant" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_publication_person" AS SELECT
            person_publikation.publikation_id::integer AS publication_id,
            person_publikation.medonline_person_id::integer AS person_id
        FROM
            research.person_publikation
        INNER JOIN
            research.publikation r_p
            ON person_publikation.publikation_id::integer = r_p.publikation_id::integer
        INNER JOIN
            campusonline.personen co_p
            ON person_publikation.medonline_person_id::integer = co_p.pers_nr::integer
        ''',
        '''
        CREATE UNIQUE INDEX research_publication_person_idx ON "public"."research_publication_person" ("publication_id", "person_id");
        ''',
        '''
        CREATE INDEX research_publication_person_publication_id_idx ON "public"."research_publication_person" ("publication_id");
        ''',
        '''
        CREATE INDEX research_publication_person_person_id_idx ON "public"."research_publication_person" ("person_id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_publication_organization" AS SELECT DISTINCT
            orgeinheit_publikation.publikation_id::integer AS publication_id,
            orgeinheit_publikation.medonline_id::integer AS organization_id
        FROM
            research.orgeinheit_publikation
        INNER JOIN
            research.publikation r_p
            ON orgeinheit_publikation.publikation_id::integer = r_p.publikation_id::integer
        INNER JOIN
            campusonline.organisationen co_o
            ON orgeinheit_publikation.medonline_id::integer = co_o.nr::integer
        ''',
        '''
        CREATE UNIQUE INDEX research_publication_organization_idx ON "public"."research_publication_organization" ("publication_id", "organization_id");
        ''',
        '''
        CREATE INDEX research_publication_organization_publication_id_idx ON "public"."research_publication_organization" ("publication_id");
        ''',
        '''
        CREATE INDEX research_publication_organization_organization_id_idx ON "public"."research_publication_organization" ("organization_id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_publicationcategory" AS SELECT
            PUBLIKATION_TYP_ID::integer AS id,
            PUBLIKATION_TYP_DE AS name
        FROM
            "research"."publikation_typ";
        ''',
        '''
        CREATE UNIQUE INDEX research_publicationcategory_id_idx ON "public"."research_publicationcategory" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_publicationdocument" AS SELECT
            PUBLIKATION_DOKUMENTTYP_ID::integer AS id,
            hstore(
                ARRAY['de', 'en'],
                ARRAY[PUBLIKATION_DOKUMENTTYP_DE, PUBLIKATION_DOKUMENTTYP_EN]
            ) AS name
        FROM
            "research"."publikation_dokumenttyp";
        ''',
        '''
        CREATE UNIQUE INDEX research_publicationdocument_id_idx ON "public"."research_publicationdocument" ("id");
        ''',
        '''
        CREATE MATERIALIZED VIEW "public"."research_publication" AS SELECT
            PUBLIKATION_ID::integer AS id,
            TITEL AS title,
            regexp_split_to_array(trim(both ' ' from AUTOR), ';\s*') AS authors,
            JAHR::integer AS year,
            QUELLE AS source,
            PUBLIKATION_TYP_ID::integer AS category_id,
            PUBLIKATION_DOKUMENTTYP_ID::integer AS document_id,
            SCI_ID AS sci,
            PUBMED_ID AS pubmed,
            DOI AS doi,
            PMC_ID AS pmc,
            ABSTRACT AS abstract_bytes
        FROM
            "research"."publikation"
        ''',
        '''
        CREATE UNIQUE INDEX research_publication_id_idx ON "public"."research_publication" ("id");
        ''',
        '''
        CREATE INDEX research_publication_year_idx ON "public"."research_publication" ("year");
        ''',
        '''
        CREATE INDEX research_publication_category_id_idx ON "public"."research_publication" ("category_id");
        ''',
        '''
        CREATE INDEX research_publication_document_id_idx ON "public"."research_publication" ("document_id");
        ''',
    ]
    reverse = [
        '''
        DROP INDEX IF EXISTS research_publication_document_id_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_category_id_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_year_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_id_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_id_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_publication";
        ''',
        '''
        DROP INDEX IF EXISTS research_publicationdocument_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_publicationdocument";
        ''',
        '''
        DROP INDEX IF EXISTS research_publicationcategory_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_publicationcategory";
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_organization_organization_id_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_organization_publication_id_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_organization_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_publication_organization";
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_person_person_id_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_person_publication_id_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_publication_person_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_publication_person";
        ''',
        '''
        DROP INDEX IF EXISTS research_projectgrant_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_projectgrant";
        ''',
        '''
        DROP INDEX IF EXISTS research_projectevent_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_projectevent";
        ''',
        '''
        DROP INDEX IF EXISTS research_projectstudy_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_projectstudy";
        ''',
        '''
        DROP INDEX IF EXISTS research_language_iso_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_language_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_language";
        ''',
        '''
        DROP INDEX IF EXISTS research_projectstatus_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_projectstatus";
        ''',
        '''
        DROP INDEX IF EXISTS research_project_funder_funder_id_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_project_funder_project_id_idx;
        ''',
        '''
        DROP INDEX IF EXISTS research_project_funder_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_project_funder";
        ''',
        '''
        DROP INDEX IF EXISTS research_project_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_project";
        ''',
        '''
        DROP INDEX IF EXISTS research_projectpartnerfunction_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_projectpartnerfunction";
        ''',
        '''
        DROP INDEX IF EXISTS research_country_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_country";
        ''',
        '''
        DROP INDEX IF EXISTS research_fundercategory_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_fundercategory";
        ''',
        '''
        DROP INDEX IF EXISTS research_funder_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_funder";
        ''',
        '''
        DROP INDEX IF EXISTS research_projectresearch_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_projectresearch";
        ''',
        '''
        DROP INDEX IF EXISTS research_projectcategory_id_idx;
        ''',
        '''
        DROP MATERIALIZED VIEW IF EXISTS "public"."research_projectcategory";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."publikation";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."publikation_dokumenttyp";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."publikation_typ";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."orgeinheit_publikation";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."person_publikation";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."vergabe_art";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."veranstaltung_art";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."studie_art";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."sprache";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."projekt_status";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."projekt_geldgeber";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."projekt";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."projekt_typ";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."org_partner_projektfunktion";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."land";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."geldgeber_typ";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."geldgeber";
        ''',
        '''
        DROP FOREIGN TABLE IF EXISTS "research"."forschung_art";
        ''',
    ]

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            forward,
            reverse
        )
    ]