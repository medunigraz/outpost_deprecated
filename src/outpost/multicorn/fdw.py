import logging
import os

import sqlalchemy
from multicorn.sqlalchemyfdw import SqlAlchemyFdw
from sqlalchemy import create_engine
from sqlalchemy.dialects import registry

logger = logging.getLogger(__name__)


class OutpostFdw(SqlAlchemyFdw):

    engine = {
        'pool_pre_ping': True,
    }

    @staticmethod
    def create_engine(url):
        logger.info(f'Calling monkey patched create_engine for {url}')
        return create_engine(url, **OutpostFdw.engine)

    def __init__(self, *args, **kwargs):
        if 'NLS_LANG' not in os.environ:
            logger.info('NLS_LANG not found in environment, updating ...')
            os.environ['NLS_LANG'] = '.UTF8'
        logger.info('Registering custom sqlalchemy dialects ...')
        registry.register(
            'oracle.pyodbc', 'outpost.multicorn.pyodbc', 'OracleDialect_pyodbc'
        )
        super(OutpostFdw, self).__init__(*args, **kwargs)


# Monkey patch create_engine in multicorn/sqlalchemy
sqlalchemy.create_engine = OutpostFdw.create_engine
