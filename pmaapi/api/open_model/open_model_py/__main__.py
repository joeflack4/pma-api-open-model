#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Open Model to SqlAlchemy"""
from sys import stderr
from os.path import isfile
from copy import copy
from itertools import repeat as iter_repeat
from pprint import PrettyPrinter
from pmaapi.config import MODEL_FILE  # Testing
from pmaapi.api.open_model.open_model_py.definitions.error \
    import OpenModelException, UnsupportedFileTypeException, \
    UnexpectedDataTypeException, InvalidSchemaException
from pmaapi.api.open_model.open_model_py.definitions.abstractions \
    import read_contents, inverse_filter_dict, yaml_load_clean, yaml_dump_clean


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

    def serialize_to_yaml(self, model):
        """Serialize Python dictionary to YAML string.

        Side Effects:
            self.yaml
        """
        self.yaml = yaml_dump_clean(model)

    def serialize_to_sqlalchemy(self, model):  # TODO: Last to create.
        """Serialize Python dictionary to a dictionary of SqlAlchemy objects.

        Side Effects:
            self.sqlalchemy
        """
        self.sqlalchemy = model

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
        self.serialize_to_yaml(copy(data))  # 3
        self.serialize_to_sqlalchemy(copy(data))  # 4


if __name__ == '__main__':  # Testing
    # TODO: Implement CLI and use file path as follows.
    #   /Users/joeflack4/projects/pma-api/pmaapi/model/model.yaml
    pp = PrettyPrinter(indent=0)
    try:
        mdl = OpenModel()
        mdl.load(MODEL_FILE)
        print(mdl.sqlalchemy)
        # pp.pprint(mdl.custom_fields)
        # print(mdl.yaml)
        # pp.pprint(mdl.dict['models']['indicators'])
    except OpenModelException as exc:
        print(exc, file=stderr)
    # pass
