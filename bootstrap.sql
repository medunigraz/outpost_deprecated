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

CREATE SERVER sqlalchemy
    FOREIGN DATA WRAPPER multicorn
    OPTIONS (
        wrapper 'outpost.fdw.OutpostFdw'
    );

GRANT USAGE ON FOREIGN SERVER sqlalchemy TO "api.medunigraz.at";

CREATE OR REPLACE FUNCTION multicorn_check_plpython3u() RETURNS VOID AS $$
BEGIN
    NULL;
END;
$$ LANGUAGE plpgsql;
