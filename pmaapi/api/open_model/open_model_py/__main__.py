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
        exc2 = 'UnsupportedDataFormatException: Apologies, but format \'{}\''\
               ' is not yet supported.'.format(file_ext)
        exc3 = 'UnsupportedDataFormatException: Format \'{}\' is not ' \
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
            raise UnsupportedFileTypeException(exc2)
        else:
            raise UnsupportedFileTypeException(exc3)

    def _load_serialized(self, data):
        # 1. Set data in dictionary format.
        model, self.source_data, self.source, self.data, self.dict, \
            = iter_repeat(copy(data), 5)
        # 2. Set key model model meta-attribute properties.
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
        self.custom_fields = {
            'customFields': inverse_filter_dict(dictionary=model,
                                                keys=OpenModel.MODEL_ROOT_KEYS)
        }
        # 3. Set data in yaml format.
        self.yaml = yaml_dump_clean(self.dict)
        # 4. Set data in SqlAlchemy format.
        # self.sqlalchemy = ''  # TODO: Last to create.


if __name__ == '__main__':  # Testing
    # TODO: Implement CLI and use file path as follows.
    #   /Users/joeflack4/projects/pma-api/pmaapi/model/model.yaml
    pp = PrettyPrinter(indent=0)
    try:
        mdl = OpenModel()
        mdl.load(MODEL_FILE)
        pp.pprint(mdl.custom_fields)
        # print(model.yaml)
        # print(model.sqlalchemy)
        # pp.pprint(mdl.dict['models']['indicators'])
    except OpenModelException as exc:
        print(exc, file=stderr)
    # pass
