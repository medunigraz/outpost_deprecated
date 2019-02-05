# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-12 15:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_replaceableentity'),
    ]

    forward = [
        '''
        CREATE OR REPLACE FUNCTION "public"."html_unescape"(t text)
        RETURNS text AS
        $BODY$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN
                SELECT DISTINCT "re"."character", "re"."name"
                FROM
                    "public"."base_replaceableentity" "re"
                    INNER JOIN (
                        SELECT name[1] "name"
                        FROM REGEXP_MATCHES(t, '&([A-Za-z]+?);', 'g') r(name)
                    ) s ON "re"."name" = "s"."name"
            LOOP
                t := REPLACE(t, '&' || r.name || ';', r."character");
            END LOOP;

            FOR r IN
                SELECT DISTINCT
                    hex[1] hex,
                    ('x' || REPEAT('0', 8 - LENGTH(hex[1])) || hex[1])::bit(32)::int codepoint
                FROM REGEXP_MATCHES(t, '&#x([0-9a-f]{1,8}?);', 'gi') s(hex)
            LOOP
                t := REGEXP_REPLACE(t, '&#x' || r.hex || ';', CHR(r.codepoint), 'gi');
            END LOOP;

            FOR r IN
                SELECT DISTINCT
                    CHR(codepoint[1]::int) ch,
                    codepoint[1] codepoint
                FROM REGEXP_MATCHES(t, '&#([0-9]{1,10}?);', 'g') s(codepoint)
            LOOP
                t := REPLACE(t, '&#' || r.codepoint || ';', r.ch);
            END LOOP;

            RETURN t;
        END;
        $BODY$
        LANGUAGE plpgsql IMMUTABLE
        COST 100;
        ''',
    ]

    reverse = [
        '''
        DROP FUNCTION "public"."html_unescape"(text);
        ''',
    ]

    def forwards_func(apps, schema_editor):
        ReplaceableEntity = apps.get_model('base', 'ReplaceableEntity')
        db_alias = schema_editor.connection.alias
        ReplaceableEntity.objects.using(db_alias).bulk_create([
            ReplaceableEntity('AElig', b'\xc3\x86'),
            ReplaceableEntity('Aacute', b'\xc3\x81'),
            ReplaceableEntity('Acirc', b'\xc3\x82'),
            ReplaceableEntity('Agrave', b'\xc3\x80'),
            ReplaceableEntity('Alpha', b'\xce\x91'),
            ReplaceableEntity('Aring', b'\xc3\x85'),
            ReplaceableEntity('Atilde', b'\xc3\x83'),
            ReplaceableEntity('Auml', b'\xc3\x84'),
            ReplaceableEntity('Beta', b'\xce\x92'),
            ReplaceableEntity('Ccedil', b'\xc3\x87'),
            ReplaceableEntity('Chi', b'\xce\xa7'),
            ReplaceableEntity('Dagger', b'\xe2\x80\xa1'),
            ReplaceableEntity('Delta', b'\xce\x94'),
            ReplaceableEntity('ETH', b'\xc3\x90'),
            ReplaceableEntity('Eacute', b'\xc3\x89'),
            ReplaceableEntity('Ecirc', b'\xc3\x8a'),
            ReplaceableEntity('Egrave', b'\xc3\x88'),
            ReplaceableEntity('Epsilon', b'\xce\x95'),
            ReplaceableEntity('Eta', b'\xce\x97'),
            ReplaceableEntity('Euml', b'\xc3\x8b'),
            ReplaceableEntity('Gamma', b'\xce\x93'),
            ReplaceableEntity('Iacute', b'\xc3\x8d'),
            ReplaceableEntity('Icirc', b'\xc3\x8e'),
            ReplaceableEntity('Igrave', b'\xc3\x8c'),
            ReplaceableEntity('Iota', b'\xce\x99'),
            ReplaceableEntity('Iuml', b'\xc3\x8f'),
            ReplaceableEntity('Kappa', b'\xce\x9a'),
            ReplaceableEntity('Lambda', b'\xce\x9b'),
            ReplaceableEntity('Mu', b'\xce\x9c'),
            ReplaceableEntity('Ntilde', b'\xc3\x91'),
            ReplaceableEntity('Nu', b'\xce\x9d'),
            ReplaceableEntity('OElig', b'\xc5\x92'),
            ReplaceableEntity('Oacute', b'\xc3\x93'),
            ReplaceableEntity('Ocirc', b'\xc3\x94'),
            ReplaceableEntity('Ograve', b'\xc3\x92'),
            ReplaceableEntity('Omega', b'\xce\xa9'),
            ReplaceableEntity('Omicron', b'\xce\x9f'),
            ReplaceableEntity('Oslash', b'\xc3\x98'),
            ReplaceableEntity('Otilde', b'\xc3\x95'),
            ReplaceableEntity('Ouml', b'\xc3\x96'),
            ReplaceableEntity('Phi', b'\xce\xa6'),
            ReplaceableEntity('Pi', b'\xce\xa0'),
            ReplaceableEntity('Prime', b'\xe2\x80\xb3'),
            ReplaceableEntity('Psi', b'\xce\xa8'),
            ReplaceableEntity('Rho', b'\xce\xa1'),
            ReplaceableEntity('Scaron', b'\xc5\xa0'),
            ReplaceableEntity('Sigma', b'\xce\xa3'),
            ReplaceableEntity('THORN', b'\xc3\x9e'),
            ReplaceableEntity('Tau', b'\xce\xa4'),
            ReplaceableEntity('Theta', b'\xce\x98'),
            ReplaceableEntity('Uacute', b'\xc3\x9a'),
            ReplaceableEntity('Ucirc', b'\xc3\x9b'),
            ReplaceableEntity('Ugrave', b'\xc3\x99'),
            ReplaceableEntity('Upsilon', b'\xce\xa5'),
            ReplaceableEntity('Uuml', b'\xc3\x9c'),
            ReplaceableEntity('Xi', b'\xce\x9e'),
            ReplaceableEntity('Yacute', b'\xc3\x9d'),
            ReplaceableEntity('Yuml', b'\xc5\xb8'),
            ReplaceableEntity('Zeta', b'\xce\x96'),
            ReplaceableEntity('aacute', b'\xc3\xa1'),
            ReplaceableEntity('acirc', b'\xc3\xa2'),
            ReplaceableEntity('acute', b'\xc2\xb4'),
            ReplaceableEntity('aelig', b'\xc3\xa6'),
            ReplaceableEntity('agrave', b'\xc3\xa0'),
            ReplaceableEntity('alefsym', b'\xe2\x84\xb5'),
            ReplaceableEntity('alpha', b'\xce\xb1'),
            ReplaceableEntity('amp', b'&'),
            ReplaceableEntity('and', b'\xe2\x88\xa7'),
            ReplaceableEntity('ang', b'\xe2\x88\xa0'),
            ReplaceableEntity('aring', b'\xc3\xa5'),
            ReplaceableEntity('asymp', b'\xe2\x89\x88'),
            ReplaceableEntity('atilde', b'\xc3\xa3'),
            ReplaceableEntity('auml', b'\xc3\xa4'),
            ReplaceableEntity('bdquo', b'\xe2\x80\x9e'),
            ReplaceableEntity('beta', b'\xce\xb2'),
            ReplaceableEntity('brvbar', b'\xc2\xa6'),
            ReplaceableEntity('bull', b'\xe2\x80\xa2'),
            ReplaceableEntity('cap', b'\xe2\x88\xa9'),
            ReplaceableEntity('ccedil', b'\xc3\xa7'),
            ReplaceableEntity('cedil', b'\xc2\xb8'),
            ReplaceableEntity('cent', b'\xc2\xa2'),
            ReplaceableEntity('chi', b'\xcf\x87'),
            ReplaceableEntity('circ', b'\xcb\x86'),
            ReplaceableEntity('clubs', b'\xe2\x99\xa3'),
            ReplaceableEntity('cong', b'\xe2\x89\x85'),
            ReplaceableEntity('copy', b'\xc2\xa9'),
            ReplaceableEntity('crarr', b'\xe2\x86\xb5'),
            ReplaceableEntity('cup', b'\xe2\x88\xaa'),
            ReplaceableEntity('curren', b'\xc2\xa4'),
            ReplaceableEntity('dArr', b'\xe2\x87\x93'),
            ReplaceableEntity('dagger', b'\xe2\x80\xa0'),
            ReplaceableEntity('darr', b'\xe2\x86\x93'),
            ReplaceableEntity('deg', b'\xc2\xb0'),
            ReplaceableEntity('delta', b'\xce\xb4'),
            ReplaceableEntity('diams', b'\xe2\x99\xa6'),
            ReplaceableEntity('divide', b'\xc3\xb7'),
            ReplaceableEntity('eacute', b'\xc3\xa9'),
            ReplaceableEntity('ecirc', b'\xc3\xaa'),
            ReplaceableEntity('egrave', b'\xc3\xa8'),
            ReplaceableEntity('empty', b'\xe2\x88\x85'),
            ReplaceableEntity('emsp', b'\xe2\x80\x83'),
            ReplaceableEntity('ensp', b'\xe2\x80\x82'),
            ReplaceableEntity('epsilon', b'\xce\xb5'),
            ReplaceableEntity('equiv', b'\xe2\x89\xa1'),
            ReplaceableEntity('eta', b'\xce\xb7'),
            ReplaceableEntity('eth', b'\xc3\xb0'),
            ReplaceableEntity('euml', b'\xc3\xab'),
            ReplaceableEntity('euro', b'\xe2\x82\xac'),
            ReplaceableEntity('exist', b'\xe2\x88\x83'),
            ReplaceableEntity('fnof', b'\xc6\x92'),
            ReplaceableEntity('forall', b'\xe2\x88\x80'),
            ReplaceableEntity('frac12', b'\xc2\xbd'),
            ReplaceableEntity('frac14', b'\xc2\xbc'),
            ReplaceableEntity('frac34', b'\xc2\xbe'),
            ReplaceableEntity('frasl', b'\xe2\x81\x84'),
            ReplaceableEntity('gamma', b'\xce\xb3'),
            ReplaceableEntity('ge', b'\xe2\x89\xa5'),
            ReplaceableEntity('gt', b'>'),
            ReplaceableEntity('hArr', b'\xe2\x87\x94'),
            ReplaceableEntity('harr', b'\xe2\x86\x94'),
            ReplaceableEntity('hearts', b'\xe2\x99\xa5'),
            ReplaceableEntity('hellip', b'\xe2\x80\xa6'),
            ReplaceableEntity('iacute', b'\xc3\xad'),
            ReplaceableEntity('icirc', b'\xc3\xae'),
            ReplaceableEntity('iexcl', b'\xc2\xa1'),
            ReplaceableEntity('igrave', b'\xc3\xac'),
            ReplaceableEntity('image', b'\xe2\x84\x91'),
            ReplaceableEntity('infin', b'\xe2\x88\x9e'),
            ReplaceableEntity('int', b'\xe2\x88\xab'),
            ReplaceableEntity('iota', b'\xce\xb9'),
            ReplaceableEntity('iquest', b'\xc2\xbf'),
            ReplaceableEntity('isin', b'\xe2\x88\x88'),
            ReplaceableEntity('iuml', b'\xc3\xaf'),
            ReplaceableEntity('kappa', b'\xce\xba'),
            ReplaceableEntity('lArr', b'\xe2\x87\x90'),
            ReplaceableEntity('lambda', b'\xce\xbb'),
            ReplaceableEntity('lang', b'\xe2\x8c\xa9'),
            ReplaceableEntity('laquo', b'\xc2\xab'),
            ReplaceableEntity('larr', b'\xe2\x86\x90'),
            ReplaceableEntity('lceil', b'\xe2\x8c\x88'),
            ReplaceableEntity('ldquo', b'\xe2\x80\x9c'),
            ReplaceableEntity('le', b'\xe2\x89\xa4'),
            ReplaceableEntity('lfloor', b'\xe2\x8c\x8a'),
            ReplaceableEntity('lowast', b'\xe2\x88\x97'),
            ReplaceableEntity('loz', b'\xe2\x97\x8a'),
            ReplaceableEntity('lrm', b'\xe2\x80\x8e'),
            ReplaceableEntity('lsaquo', b'\xe2\x80\xb9'),
            ReplaceableEntity('lsquo', b'\xe2\x80\x98'),
            ReplaceableEntity('lt', b'<'),
            ReplaceableEntity('macr', b'\xc2\xaf'),
            ReplaceableEntity('mdash', b'\xe2\x80\x94'),
            ReplaceableEntity('micro', b'\xc2\xb5'),
            ReplaceableEntity('middot', b'\xc2\xb7'),
            ReplaceableEntity('minus', b'\xe2\x88\x92'),
            ReplaceableEntity('mu', b'\xce\xbc'),
            ReplaceableEntity('nabla', b'\xe2\x88\x87'),
            ReplaceableEntity('nbsp', b'\xc2\xa0'),
            ReplaceableEntity('ndash', b'\xe2\x80\x93'),
            ReplaceableEntity('ne', b'\xe2\x89\xa0'),
            ReplaceableEntity('ni', b'\xe2\x88\x8b'),
            ReplaceableEntity('not', b'\xc2\xac'),
            ReplaceableEntity('notin', b'\xe2\x88\x89'),
            ReplaceableEntity('nsub', b'\xe2\x8a\x84'),
            ReplaceableEntity('ntilde', b'\xc3\xb1'),
            ReplaceableEntity('nu', b'\xce\xbd'),
            ReplaceableEntity('oacute', b'\xc3\xb3'),
            ReplaceableEntity('ocirc', b'\xc3\xb4'),
            ReplaceableEntity('oelig', b'\xc5\x93'),
            ReplaceableEntity('ograve', b'\xc3\xb2'),
            ReplaceableEntity('oline', b'\xe2\x80\xbe'),
            ReplaceableEntity('omega', b'\xcf\x89'),
            ReplaceableEntity('omicron', b'\xce\xbf'),
            ReplaceableEntity('oplus', b'\xe2\x8a\x95'),
            ReplaceableEntity('or', b'\xe2\x88\xa8'),
            ReplaceableEntity('ordf', b'\xc2\xaa'),
            ReplaceableEntity('ordm', b'\xc2\xba'),
            ReplaceableEntity('oslash', b'\xc3\xb8'),
            ReplaceableEntity('otilde', b'\xc3\xb5'),
            ReplaceableEntity('otimes', b'\xe2\x8a\x97'),
            ReplaceableEntity('ouml', b'\xc3\xb6'),
            ReplaceableEntity('para', b'\xc2\xb6'),
            ReplaceableEntity('part', b'\xe2\x88\x82'),
            ReplaceableEntity('permil', b'\xe2\x80\xb0'),
            ReplaceableEntity('perp', b'\xe2\x8a\xa5'),
            ReplaceableEntity('phi', b'\xcf\x86'),
            ReplaceableEntity('pi', b'\xcf\x80'),
            ReplaceableEntity('piv', b'\xcf\x96'),
            ReplaceableEntity('plusmn', b'\xc2\xb1'),
            ReplaceableEntity('pound', b'\xc2\xa3'),
            ReplaceableEntity('prime', b'\xe2\x80\xb2'),
            ReplaceableEntity('prod', b'\xe2\x88\x8f'),
            ReplaceableEntity('prop', b'\xe2\x88\x9d'),
            ReplaceableEntity('psi', b'\xcf\x88'),
            ReplaceableEntity('quot', b'"'),
            ReplaceableEntity('rArr', b'\xe2\x87\x92'),
            ReplaceableEntity('radic', b'\xe2\x88\x9a'),
            ReplaceableEntity('rang', b'\xe2\x8c\xaa'),
            ReplaceableEntity('raquo', b'\xc2\xbb'),
            ReplaceableEntity('rarr', b'\xe2\x86\x92'),
            ReplaceableEntity('rceil', b'\xe2\x8c\x89'),
            ReplaceableEntity('rdquo', b'\xe2\x80\x9d'),
            ReplaceableEntity('real', b'\xe2\x84\x9c'),
            ReplaceableEntity('reg', b'\xc2\xae'),
            ReplaceableEntity('rfloor', b'\xe2\x8c\x8b'),
            ReplaceableEntity('rho', b'\xcf\x81'),
            ReplaceableEntity('rlm', b'\xe2\x80\x8f'),
            ReplaceableEntity('rsaquo', b'\xe2\x80\xba'),
            ReplaceableEntity('rsquo', b'\xe2\x80\x99'),
            ReplaceableEntity('sbquo', b'\xe2\x80\x9a'),
            ReplaceableEntity('scaron', b'\xc5\xa1'),
            ReplaceableEntity('sdot', b'\xe2\x8b\x85'),
            ReplaceableEntity('sect', b'\xc2\xa7'),
            ReplaceableEntity('shy', b'\xc2\xad'),
            ReplaceableEntity('sigma', b'\xcf\x83'),
            ReplaceableEntity('sigmaf', b'\xcf\x82'),
            ReplaceableEntity('sim', b'\xe2\x88\xbc'),
            ReplaceableEntity('spades', b'\xe2\x99\xa0'),
            ReplaceableEntity('sub', b'\xe2\x8a\x82'),
            ReplaceableEntity('sube', b'\xe2\x8a\x86'),
            ReplaceableEntity('sum', b'\xe2\x88\x91'),
            ReplaceableEntity('sup', b'\xe2\x8a\x83'),
            ReplaceableEntity('sup1', b'\xc2\xb9'),
            ReplaceableEntity('sup2', b'\xc2\xb2'),
            ReplaceableEntity('sup3', b'\xc2\xb3'),
            ReplaceableEntity('supe', b'\xe2\x8a\x87'),
            ReplaceableEntity('szlig', b'\xc3\x9f'),
            ReplaceableEntity('tau', b'\xcf\x84'),
            ReplaceableEntity('there4', b'\xe2\x88\xb4'),
            ReplaceableEntity('theta', b'\xce\xb8'),
            ReplaceableEntity('thetasym', b'\xcf\x91'),
            ReplaceableEntity('thinsp', b'\xe2\x80\x89'),
            ReplaceableEntity('thorn', b'\xc3\xbe'),
            ReplaceableEntity('tilde', b'\xcb\x9c'),
            ReplaceableEntity('times', b'\xc3\x97'),
            ReplaceableEntity('trade', b'\xe2\x84\xa2'),
            ReplaceableEntity('uArr', b'\xe2\x87\x91'),
            ReplaceableEntity('uacute', b'\xc3\xba'),
            ReplaceableEntity('uarr', b'\xe2\x86\x91'),
            ReplaceableEntity('ucirc', b'\xc3\xbb'),
            ReplaceableEntity('ugrave', b'\xc3\xb9'),
            ReplaceableEntity('uml', b'\xc2\xa8'),
            ReplaceableEntity('upsih', b'\xcf\x92'),
            ReplaceableEntity('upsilon', b'\xcf\x85'),
            ReplaceableEntity('uuml', b'\xc3\xbc'),
            ReplaceableEntity('weierp', b'\xe2\x84\x98'),
            ReplaceableEntity('xi', b'\xce\xbe'),
            ReplaceableEntity('yacute', b'\xc3\xbd'),
            ReplaceableEntity('yen', b'\xc2\xa5'),
            ReplaceableEntity('yuml', b'\xc3\xbf'),
            ReplaceableEntity('zeta', b'\xce\xb6'),
            ReplaceableEntity('zwj', b'\xe2\x80\x8d'),
            ReplaceableEntity('zwnj', b'\xe2\x80\x8c'),
        ])

    def reverse_func(apps, schema_editor):
        ReplaceableEntity = apps.get_model('base', 'ReplaceableEntity')
        db_alias = schema_editor.connection.alias
        ReplaceableEntity.objects.using(db_alias).all().delete()

    operations = [
        migrations.RunSQL(
            forward,
            reverse
        ),
        migrations.RunPython(
            forwards_func,
            reverse_func
        ),
    ]