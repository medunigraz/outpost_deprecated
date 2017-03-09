import sqlalchemy.dialects.postgresql.base
from sqlalchemy.dialects.postgresql.array import ARRAY

sqlalchemy.dialects.postgresql.base.ARRAY = ARRAY

from multicorn.sqlalchemyfdw import SqlAlchemyFdw
from sqlalchemy.dialects import registry


class OutpostFdw(SqlAlchemyFdw):

    def __init__(self, *args, **kwargs):
        registry.register(
            'oracle.pyodbc', 'outpost.pyodbc', 'OracleDialect_pyodbc'
        )
        super(OutpostFdw, self).__init__(*args, **kwargs)
