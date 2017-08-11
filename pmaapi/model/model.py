#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Temporary SqlAlchemy Models."""
from sys import stderr
from copy import copy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Boolean, Integer, String, Float, \
    BigInteger, Date
from sqlalchemy.sql.functions import func as sqlalchemy_func
from flask_sqlalchemy import SQLAlchemy
from pmaapi.__main__ import FLASK_APP
from pmaapi.definitions.error import DatabaseException
# from sqlalchemy.exc import ProgrammingError, IntegrityError
# from pmaapi.definitions.error import raise_database_exception


# db = SQLAlchemy(FLASK_APP)
# db.Base = declarative_base()
now = sqlalchemy_func.now


# --- Testing and Placeholder Functions --- #
def get_current_user():
    """Get current user. Placeholder. Shouldn't even come from this class.

    Returns:
        str: Current user.
        """
    return 'System'  # Placeholder


# - TODO: Relational mapping - http://tinyurl.com/yc2j7jkg
# - TODO: Use unicode instead of string?
# - TODO: Consider autoload to reflect table attributes from what is in DB.
# SqlAlchemy ------------------------------------------------------------------
# class BaseModel(db.Model):  # TODO: Set in UTC.
class BaseModel(declarative_base()):  # TODO: Set in UTC.
    """Base Model."""
    __abstract__ = True

    created_on = Column(DateTime, nullable=False, default=now(), index=True)
    updated_on = Column(DateTime, nullable=False, default=now(),
                        onupdate=now(), index=True)
    created_by = Column(String(80), nullable=False, default='System',
                        onupdate=get_current_user(), index=True)
    updated_by = Column(String(80), nullable=False, index=True)

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self):
        return '<Model \'{}\' of id \'{}\'.>'.format(type(self).__name__, self.id)


# TODO: Define which ones are FKs (key=?).
db = SQLAlchemy(FLASK_APP)
db.Base = BaseModel
# TODO: Will I need to use copy(), or is it ok just to refer to these?
id_int = Column(BigInteger, primary_key=True, autoincrement=True, doc=None)
id_str = Column(String(500), primary_key=True, nullable=False, index=True,
                unique=True, doc=None)
fk_required_str = \
    Column(String(500), nullable=False, index=True, unique=False, doc=None)
fk_optional_str = \
    Column(String(500), nullable=True, index=True, unique=False, doc=None)
data_float = Column(Float, nullable=True, index=False, unique=False, doc=None)
_type = nonunique_label = indexable_required_nonunique_str = fk_required_str
unique_label = indexable_required_unique_str = \
    Column(String(500), nullable=False, index=True, unique=True, doc=None)
indexable_optional_unique_str = \
    Column(String(500), nullable=True, index=True, unique=True, doc=None) 
definition_optional = indexable_optional_nonunique_str = \
    Column(String(500), nullable=True, index=True, unique=False, doc=None)
_order = required_unique_order = \
    Column(Integer, unique=True, nullable=False, index=True, doc=None)
optional_unique_order = \
    Column(Integer, unique=True, nullable=True, index=True, doc=None)
optional_bool = Column(Boolean, nullable=True, index=True, doc=None)
required_bool = Column(Boolean, nullable=False, index=True, doc=None)
indexable_required_int = Column(Integer, nullable=False, index=True, doc=None)
optional_nonunique_date = \
    Column(Date, nullable=True, index=True, unique=False, doc=None)
nonunique_geo_str = \
    Column(String(1000), nullable=False, index=False, unique=False, doc=None)


class Data(BaseModel):
    """A SqlAlchemy model class."""
    __tablename__ = 'data'

    id = copy(id_int)
    value = copy(data_float)
    lowerCi = copy(data_float)
    UpperCi = copy(data_float)
    levelCi = copy(data_float)
    precision = \
        Column(Integer, nullable=True, index=False, unique=False, doc=None)
    isTotal = copy(required_bool)
    denominatorWeighted = copy(data_float)
    denominatorUnweighted = copy(data_float)
    indicator_id = copy(fk_required_str)
    survey_id = copy(fk_required_str)
    geography_id = copy(fk_required_str)
    characteristic_ids = copy(fk_required_str)


class Indicator(BaseModel):
    """A SqlAlchemy model class."""
    __tablename__ = 'indicator'

    id = copy(id_str)
    label = copy(unique_label)
    order = copy(_order)
    type = copy(indexable_required_nonunique_str)
    definition = copy(definition_optional)
    level1 = copy(indexable_required_nonunique_str)
    level2 = copy(indexable_required_nonunique_str)
    level3 = copy(indexable_required_nonunique_str)
    denominator = copy(indexable_required_nonunique_str)
    measurement_type = copy(indexable_required_nonunique_str)
    is_favorite = copy(optional_bool)
    favorite_order = copy(optional_unique_order)
    tag_ids = copy(fk_optional_str)


class Characteristic(BaseModel):
    """A SqlAlchemy model class."""
    __tablename__ = 'characteristic'

    id = copy(id_str)
    label = copy(unique_label)
    order = copy(_order)
    characteristic_group_id = copy(fk_required_str)


class CharacteristicGroup(BaseModel):
    """A SqlAlchemy model class."""
    __tablename__ = 'characteristic_group'

    id = copy(id_str)
    label = copy(unique_label)
    definition = copy(definition_optional)


class Survey(BaseModel):
    """A SqlAlchemy model class."""
    __tablename__ = 'survey'

    id = copy(id_str)
    label = copy(unique_label)
    order = copy(_order)
    type = copy(indexable_required_nonunique_str)
    year = copy(indexable_required_int)  # Date, but YYYY?
    round = copy(indexable_required_int)
    start_date = copy(optional_nonunique_date)
    end_date = copy(optional_nonunique_date)
    geography_id = copy(fk_required_str)


class Geography(BaseModel):
    """A SqlAlchemy model class."""
    __tablename__ = 'geography'

    id = copy(id_str)
    label = copy(unique_label)
    order = copy(_order)
    type = copy(_type)
    pma_code = copy(indexable_required_unique_str)
    is_country = copy(required_bool)
    countryCode = copy(indexable_optional_unique_str)
    parent_id = copy(fk_optional_str)
    gis_id = copy(fk_optional_str)
    tag_ids = copy(fk_optional_str)
    child_ids_calculated = copy(fk_optional_str)


class GIS(BaseModel):
    """A SqlAlchemy model class."""
    __tablename__ = 'gis'

    id = copy(id_str)
    type = copy(_type)
    shape = copy(nonunique_geo_str)
    proj4 = copy(nonunique_geo_str)
    geography_id = copy(fk_required_str)


class Translation(BaseModel):
    """A SqlAlchemy model class."""
    __tablename__ = 'translation'

    id = copy(id_str)  # abbr
    language = copy(indexable_required_nonunique_str)
    text = copy(indexable_required_nonunique_str)
    default = copy(optional_bool)


class Tag(BaseModel):
    """A SqlAlchemy model class."""
    __tablename__ = 'tag'

    id = copy(id_str)
    label = copy(unique_label)
    order = copy(_order)
    type = copy(_type)
    indicator_ids = copy(fk_optional_str)
    geography_ids = copy(fk_optional_str)


# --- Testing and Placeholder Functions --- #
# noinspection PyMissingConstructor
# class Modules(BaseModel):
#     """Modules."""
#     __tablename__ = 'modules'
#
    # id = Column(Integer, primary_key=True, nullable=False,
    #             autoincrement=True)
#     name = Column(String(80), unique=True, nullable=False, index=True)
#     abbreviation = Column(String(20), unique=True, nullable=False,
#                           index=True)
#     description = indexable_required_nonunique_str
#     active = Column(Boolean, nullable=False, index=True)
#
#     def __init__(self, name=None, abbreviation=None, description=None,
#                  active=None):
#         # BaseModel.__init__(self)
#         self.name = name
#         self.abbreviation = abbreviation
#         self.description = description
#         self.active = active
#
#     def __repr__(self):
#         return '<module name: {}>'.format(self.id)


# def add_module(_db, data):  # TODO: Make this a method of Module.
#     """Add module."""
#     try:
#         mod = Modules(name=data['name'], abbreviation='', description='',
#                       active=True)
#         _db.session.add(mod)
#         _db.session.commit()
#     except ProgrammingError as err:
#         msg = str(
#             err) + '\n\nAn error occurred and the DB session was rolled' \
#                    ' back. Please see stack trace for more information.'
#         raise_database_exception(_db, msg)
#     except IntegrityError as err:
#         msg = str(
#             err) + '\n\nAn error occurred and the DB session was rolled' \
#                    ' back. Please see stack trace for more information.'
#         raise_database_exception(_db, msg)


if __name__ == '__main__':  # Testing
    try:
        # DB Testing
        db.create_all()
        db.session.commit()
    except DatabaseException as exc:
        print(exc, file=stderr)
    # pass
