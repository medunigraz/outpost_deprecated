CREATE EXTENSION IF NOT EXISTS multicorn;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgrouting;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS hstore;

CREATE SERVER sqlalchemy
    FOREIGN DATA WRAPPER multicorn
    OPTIONS (
        wrapper 'outpost.multicorn.fdw.OutpostFdw'
    );

GRANT USAGE ON FOREIGN SERVER sqlalchemy TO "api.medunigraz.at";

