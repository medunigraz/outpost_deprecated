import re

from sqlalchemy.dialects.oracle.base import OracleDialect
from sqlalchemy.connectors.pyodbc import PyODBCConnector
from sqlalchemy.exc import DBAPIError


class OracleDialect_pyodbc(PyODBCConnector, OracleDialect):

    def _get_server_version_info(self, connection):
        try:
            raw = connection.scalar('SELECT * FROM v$version;')
        except DBAPIError:
            return super(OracleDialect_pyodbc, self)._get_server_version_info(connection)
        else:
            r = re.compile(r' (?P<version>[\d\.]+) ')
            version = r.search(raw).groupdict().get('version', '0')
            return tuple(map(int, version.split('.')))
