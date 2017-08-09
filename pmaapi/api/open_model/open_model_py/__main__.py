#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Open Model class definition."""
from pmaapi.config import MODEL_FILE  # For testing.
from pprint import PrettyPrinter  # For testing.
from sys import stderr
from os.path import isfile
from copy import copy
from itertools import repeat as iter_repeat
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, DateTime, Boolean, Integer, String
# from sqlalchemy.exc import ProgrammingError, IntegrityError
# from sqlalchemy.sql.functions import func as sqlalchemy_func
# from flask_sqlalchemy import SQLAlchemy
from pmaapi.api.open_model.open_model_py.definitions.error \
    import OpenModelException, UnsupportedFileTypeException, \
    UnexpectedDataTypeException, InvalidSchemaException, \
    UnimplementedFunctionalityException
from pmaapi.api.open_model.open_model_py.definitions.abstractions \
    import read_contents, inverse_filter_dict, yaml_load_clean, \
    yaml_dump_clean
from pmaapi.api.open_model.open_model_py.definitions.constants import MAPPINGS
# from pmaapi.__main__ import FLASK_APP
# from pmaapi.definitions.error import raise_database_exception


# db = SQLAlchemy(FLASK_APP)
# db.Base = declarative_base()
# now = sqlalchemy_func.now

# TODO - Remove all this stuff as it's all going to be auto-generated.
# - TODO: Relational mapping - http://tinyurl.com/yc2j7jkg
# - TODO: Use unicode instead of string?
# - TODO: Consider autoload to reflect table attributes from what is in DB.
# Class Generation ------------------------------------------------------------
# _dict = {}


# Dynamic instance attribute generation.
# class AllMyFields:
#     """Dynamic Class."""
#
#     def __init__(self, dictionary):
#         """Init."""
#         for k, v in dictionary.items():
#             setattr(self, k, v)
#
#
# # Dynamic class generation.
# # For the tuple, can use 'object' maybe, or give it a class(s).
# my_class = type('MyClass', (object, ), {'hello_world': lambda: 'hello'})
# my_instance = my_class({'name': 'my name'})

# SqlAlchemy ------------------------------------------------------------------
# class BaseModel(db.Model):  # TODO: Set in UTC.
#     """Base Model."""
#     __abstract__ = True
#
#     created_on = Column(DateTime, default=now(), index=True)
#     updated_on = Column(DateTime, default=now(), onupdate=now(), index=True)


# class Modules(BaseModel):
# class Modules(BaseModel):
#     """Modules."""
#     __tablename__ = 'modules'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(80), unique=True, nullable=False, index=True)
#     abbreviation = Column(String(20), unique=True, nullable=False,
#                           index=True)
#     description = Column(String(500), nullable=False)
#     active = Column(Boolean, nullable=False, index=True)
#
#     def __init__(self, name=None, abbreviation=None, description=None,
#                  active=None):
#         self.name = name
#         self.abbreviation = abbreviation
#         self.description = description
#         self.active = active
#
#     def __repr__(self):
#         return '<module name: {}>'.format(self.id)


# --- Testing --- #
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


# OpenModel -------------------------------------------------------------------
class OpenModel:
    """Open Model to SqlAlchemy"""

    PLANNED_SUPPORTED_FILE_TYPES = ('csv', 'json', 'xml')
    SUPPORTED_DATA_FORMATS = ('yaml',)
    # from pathlib import PurePath  # - Disabled: Not supported in Python 2.
    SUPPORTED_DATA_TYPES = (str, bytes, int)  # - Disabled: pathlib.PurePath
    MODEL_ROOT_KEYS = \
        ('baller', 'config', 'info', 'models', 'abstractModels', 'relations')
    BRAND_NAME = 'OpenModel'

    def __init__(self, source_data=None):
        """Initialize.

        Arguments:
            source_data (dict): Source data in Python dictionary serialization.
        """
        self.data, self.source_data, self.source, self.source_file_data, \
            self.source_file_path, self.dict, self.yaml, self.sqlalchemy, \
            self.open_model_version, self.config, self.info, self.models, \
            self.abstract_models, self.relations, self.custom_fields\
            = iter_repeat(None, 15)
        if source_data:
            self.load(source_data)

    def __iter__(self):
        """Returns dict with data as dict set as value to key 'open_model'."""
        yield 'open_model', self.dict

    def __str__(self):
        """Returns stringified dictionary."""
        return str(self.dict)

    def get_data(self, data_format):
        """Get data in requested format.

        Returns:
            Data in the format requested.
        """
        return self.yaml if data_format is 'yaml' \
            else self.dict if data_format in ('dict', 'dictionary') \
            else self.sqlalchemy if data_format is 'sqlalchemy' \
            else self.yaml

    def load(self, source_data):
        """Load source data.

        The pathlib.PurePath class represents os.PathLike.

        Raises:
            UnexpectedDataTypeException
        """
        err_msg = 'UnexpectedDataTypeException: Unexpected data type.'
        if type(source_data) in OpenModel.SUPPORTED_DATA_TYPES:
            if isfile(source_data):
                self._load_file(file=source_data)
            else:
                raise UnexpectedDataTypeException(err_msg)
        elif type(source_data) is dict:
            self._load_serialized(data=source_data)
        else:
            raise UnexpectedDataTypeException(err_msg)

    @staticmethod
    def serialize_to_yaml(model):
        """Serialize Python dictionary to YAML string.

        # TODO: Set in PrettyPrinter format.

        Args:
            model (dict): Python dictionary formatted model.

        Returns:
            str: YAML formatted model.
        """
        return yaml_dump_clean(model)

    @staticmethod
    def serialize_to_sqlalchemy(model):  # TODO: Last to create.
        """Serialize Python dictionary to a dictionary of SqlAlchemy objects.

        Args:
            model (dict): OpenModel format of model.

        Returns:
            dict: SqlAlchemy format of model.
        """
        # from sqlalchemy.ext.declarative import declarative_base
        # from sqlalchemy.exc import ProgrammingError, IntegrityError
        # from sqlalchemy.sql.functions import func as sqlalchemy_func
        # from flask_sqlalchemy import SQLAlchemy
        # from sqlalchemy import Column, DateTime, Boolean, Integer, String
        from sqlalchemy import Column
        # from pmaapi.api.open_model.open_model_py.definitions.error \
        #     import OpenModelException, UnsupportedFileTypeException, \
        #     UnexpectedDataTypeException, InvalidSchemaException
        # from pmaapi.api.open_model.open_model_py.definitions.abstractions \
        #     import read_contents, inverse_filter_dict, yaml_load_clean, \
        #     yaml_dump_clean
        # from pmaapi.__main__ import FLASK_APP
        # from pmaapi.definitions.error import raise_database_exception

        def _det_sqlalchemy_col_type_from_openmodel(om_type):
            """Determine column data type. None values are currently not supported.

            Args:
                om_type (str): Type as displayed in OpenModel file.

            Returns:
                (class): The matching SqlAlchemy type class.
            """
            return MAPPINGS['OPENMODEL_SQLALCHEMY']['DATA_TYPES'][om_type]

        def _det_col_type(openmodel_type):
            """Alias: _det_sqlalchemy_col_type_from_openmodel"""
            return _det_sqlalchemy_col_type_from_openmodel(openmodel_type)

        def _det_col_props(openmodel_props):
            """Determine column type properties."""
            if openmodel_props:
                if 'size_max' in openmodel_props:
                    return openmodel_props['size_max']
                else:
                    raise UnimplementedFunctionalityException(
                        'UnimplementedFunctionalityException: One or more '
                        'field type properties defined in model specification '
                        'is not yet supported.')

        def _det_col_type_and_props(openmodel_type_def):
            """Determine column type and type properties.

            Args:
                openmodel_type_def (dict): Type definition.

            Returns:
                class(params): SqlAlchemy type class with params.
            """
            data_type = _det_col_type(openmodel_type_def['name'])
            data_props = _det_col_props(openmodel_type_def['props'])
            return data_type(data_props)

        def _type(openmodel_type_def):
            """Alias: _det_col_type_and_props"""
            return _det_col_type_and_props(openmodel_type_def)

        def _to_sqlalchemy_classdef_dict(mdl_name, mdl_data):
            """Convert OpenModel model spec to SqlAlchemy.

            Any parameter using passed to Column() which uses the function
            evaluation 'set_and_true()' will return True if the specified key
            is in the model, and its value is set to either TRUE, true, or True
            , without quotes.

            Args:
                mdl_name (str): Name of model as defined in spec.
                mdl_data (dict): Python dictionary representation of the model.

            Returns:
                dict: SqlAlchemy class definition as Python dictionary.
            """
            mapping = MAPPINGS['OPENMODEL_SQLALCHEMY']['COLUMN_KEYS']
            # noinspection PyCompatibility
            return {
                **{'__tablename__': mdl_name},
                **{field: Column(
                    _type(fld_data['type']),  # (1) Data Type
                    primary_key=fld_data['key'] == 'PK' or False,  # (2) PK
                    **{kwd: fld_data.pop(kwd, None) for kwd in  # (3) Kwargs
                       [mapping[key] for key in fld_data
                        if key in mapping]}
                ) for field, fld_data in mdl_data['fields'].items()}
            }

        def _render_classes(classes):
            """Render classes."""
            # TODO: Use abstract models and create superclasses. Then pass in.
            # the 2nd, tuple argument when creating the table classes.
            # class BaseModel(db.Model):  # TODO: Set in UTC.
            #     """Base Model."""
            #     __abstract__ = True
            #     created_on = Column(DateTime, default=now(), index=True)
            #     updated_on = Column(DateTime, default=now(), onupdate=now(),
            #                         index=True)

            # TODO Do this for: sqlalchemy_class_defs. Then test.
            # for item in table_classes:
            #     table_class_def = type(
            #         'ExampleTableClass' + str(i), (BaseModel,), item
            #     )
            #     # noinspection PyTypeChecker
            #     self.sqlalchemy.append(table_class_def)
            #     i += 1
            return classes

        # Testing
        # db = SQLAlchemy(FLASK_APP)
        # db.Base = declarative_base()
        # Testing

        # TODO: Handle data type value mapping, e.g. 'now'.
        # now = sqlalchemy_func.now

        sqlalchemy_base_representations = {
            'abstract_classes': [],  # TODO
            'uninherited_classes': [_to_sqlalchemy_classdef_dict(name, defn)
                                    for name, defn in model['models'].items()]
        }

        # pp = PrettyPrinter(indent=2)
        # pp.pprint(table['name'].index)

        # Testing
        # db2.create_all()  # Magically knows that 'tables' has classes.
        # db2.session.commit()
        # Testing

        return _render_classes(sqlalchemy_base_representations)
        # TODO: Return a dictionary only. db.<whatever> can be done after.

    def _load_file(self, file):
        """Loads file, and runs initialization in Python dictionary format.

        Side Effects:
            self.__init__: Initializes with source file data.
            self.source_file_path, self.source_file_data: Set.

        Raises:
            UnexpectedException, UnsupportedFileTypeException
        """
        file_ext = file.rpartition('.')[-1]
        exc1 = 'UnsupportedDataFormatException: Apologies, but format \'{}\''\
               ' is not yet supported.'.format(file_ext)
        exc2 = 'UnsupportedDataFormatException: Format \'{}\' is not ' \
               'supported.'.format(file_ext)

        if file_ext in OpenModel.SUPPORTED_DATA_FORMATS:
            data = None
            if file_ext == 'yaml':
                data = yaml_load_clean(file)
            elif file_ext == 'json':  # Planned
                pass
            elif file_ext == 'xml':  # Planned
                pass
            elif file_ext == 'csv':  # Planned
                pass
            self.__init__(source_data=copy(data))
            self.source_file_path = str(copy(file))
            self.source_file_data = read_contents(file)
        elif file_ext in OpenModel.PLANNED_SUPPORTED_FILE_TYPES:
            raise UnsupportedFileTypeException(exc1)
        else:
            raise UnsupportedFileTypeException(exc2)

    def _set_meta_attributes(self, model):
        """Set primary model meta-attribute properties.

        OpenModel spec specifies that primary model meta-attributes keys reside
        in the root of a hierarchical model.

        Side Effects:
            self.open_model_version, self.config, self.info, self.models,
            self.abstract_models, self.relations

        Raises:
            InvalidSchemaException
        """
        try:
            self.open_model_version, self.config, self.info, self.models, \
                self.abstract_models, self.relations \
                = model['baller'], model['config'], model['info'], \
                model['models'], model['abstractModels'], model['relations']
        except KeyError:
            msg = 'InvalidSchemaException: An error occurred while attempting'\
                  ' to read data model. Please checked that root keys conform'\
                  ' to {} standard.'.format(OpenModel.BRAND_NAME)
            raise InvalidSchemaException(msg)

    def _set_custom_meta_attributes(self, model):
        """Set custom primary meta attributes.

        OpenModel spec specifies that primary model meta-attributes keys reside
        in the root of a hierarchical model. Custom attributes are any
        attributes in the model root which are not specified by the spec.

        Side Effects:
            self.custom_fields
        """
        self.custom_fields = {
            'customFields': inverse_filter_dict(dictionary=model,
                                                keys=OpenModel.MODEL_ROOT_KEYS)
        }

    def _set_custom_fields(self, model):
        """Alias: _set_custom_meta_attributes."""
        self._set_custom_meta_attributes(model)

    def _set_dict_format_attribute_aliases(self, data):
        """Set dictionary format instance attributes.

        Set dictionary format instance attribute self.dict and other instance
        attribute aliases for that attribute.

        Side Effects:
            self.source_data, self.source, self.data, self.dict
        """
        self.source_data, self.source, self.data, self.dict, \
            = iter_repeat(copy(data), 4)

    def _load_serialized(self, data):
        """Loads seralized data into instance.

        Side Effects:
            (1) Sets dictionary format instance attribute self.dict and other
            instance attribute aliases for that attribute, (2) Sets custom
            specified by the data but not understood by the OpenModel spec, (3)
            Serializes Python dictionary to YAML string, (4) Serializes Python
            dictionary to a dictionary of SqlAlchemy objects.

        Raises:
            UnexpectedException, UnsupportedFileTypeException
        """
        self._set_dict_format_attribute_aliases(copy(data))  # 1
        self._set_custom_fields(copy(data))  # 2
        self.yaml = self.serialize_to_yaml(copy(data))  # 3
        self.sqlalchemy = self.serialize_to_sqlalchemy(copy(data))  # 4


if __name__ == '__main__':  # Testing
    # TODO: Implement CLI and use file path as follows.
    #   /Users/joeflack4/projects/pma-api/pmaapi/model/model.yaml

    try:
        # OpenModel Testing
        mdl = OpenModel()
        mdl.load(MODEL_FILE)
        pp2 = PrettyPrinter(indent=0)
        # print(mdl.sqlalchemy)
        # print(mdl.yaml)
        # pp2.pprint(mdl.custom_fields)
        # pp2.pprint(mdl.dict['models']['indicators'])

        # SqlAlchemy Testing
        # example = Modules()
        # print(dir(example))
        # print(example.created_on)

        # Class Generation Teting
        class_gen = AllMyFields({'a': 1, 'b': 2})
        print(class_gen.a)
    except OpenModelException as exc:
        print(exc, file=stderr)
    # pass
