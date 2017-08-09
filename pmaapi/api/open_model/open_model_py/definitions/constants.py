"""Constant definitions.

MAPPINGS (dict): Mappings used by the package.
  - OPENMODEL_SQLALCHEMY (dict): Mappings between OpenModel and SqlAlchemy.
    - COLUMN_KEYS (dict): Column key name mappings. Non-implemented mappings
      are currently commented out.
    - DATA_TYPES (dict): Data type mappings. Values of 'None' indicate that the
      data type has not yet been implemented by OpenModel spec.
"""
from sqlalchemy import Date, DateTime, Boolean, Integer, String, BigInteger, \
    Binary, Float, SmallInteger, Time, Unicode


MAPPINGS = {
    'OPENMODEL_SQLALCHEMY': {
        'COLUMN_KEYS': {
            'autoIncrement': 'autoincrement',
            'default': 'default',
            'description': 'doc',
            'index': 'index',
            # 'key': 'key',  # Not yet implemented. Conflicts with PK setup
            'nullable': 'nullable',
            'onUpdate': 'onupdate',
            'serverDefault': 'server_default',
            'serverOnUpdate': 'server_onupdate',
            'system': 'system',
            'unique': 'unique'
        },
        'DATA_TYPES': {
            'ARRAY': None,
            'BIGINT': BigInteger,
            'BINARY': Binary,
            'BLOB': None,
            'BOOL': Boolean,
            'BOOLEAN': Boolean,
            'CHAR': String,
            'CLOB': None,
            'DATE': Date,
            'DATETIME': DateTime,
            'DECIMAL': Float,
            'FLOAT': Float,
            'INT': Integer,
            'INTEGER': Integer,
            'JSON': None,
            'LONG': BigInteger,
            'NCHAR': String,
            'NVARCHAR': String,
            'NUMERIC': Float,
            'REAL': Float,
            'SMALLINT': SmallInteger,
            'TEXT': String,
            'TIME': Time,
            'TIMESTAMP': None,
            'UNICODE': Unicode,
            'VARBINARY': None,
            'VARCHAR': String,
        }
    }
}
