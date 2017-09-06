CREATE EXTENSION IF NOT EXISTS plpython3u;
CREATE EXTENSION IF NOT EXISTS multicorn;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgrouting;


CREATE OR REPLACE FUNCTION html_unescape (input text)
    RETURNS text
    AS $$
    if 'html' in SD:
        html = SD['html']
    else:
        import html
        SD['html'] = html

    return html.unescape(input)
    $$ LANGUAGE plpython3u;
