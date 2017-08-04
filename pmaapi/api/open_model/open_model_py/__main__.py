#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Open Model to SqlAlchemy"""
from sys import stderr
from os.path import isfile
from copy import copy
from itertools import repeat as iter_repeat
from yaml import load as yaml_load, YAMLError
from pmaapi.config import MODEL_FILE, SUPPORTED_DATA_FORMATS, \
    SUPPORTED_DATA_TYPES, PLANNED_SUPPORTED_FILE_TYPES
from pmaapi.api.open_model.open_model_py.definitions.error \
    import OpenModelException, UnsupportedFileTypeException, \
    UnexpectedDataTypeException
from pmaapi.api.open_model.open_model_py.definitions.abstractions \
    import open_and_read


class OpenModel:
    """Open Model to SqlAlchemy"""

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
        if type(source_data) in SUPPORTED_DATA_TYPES:
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
        exc1 = 'YAMLError: An unexpected error occurred when attempting to ' \
               'read supplied YAML.'
        exc2 = 'UnsupportedDataFormatException: Apologies, but format \'{}\''\
               ' is not yet supported.'.format(file_ext)
        exc3 = 'UnsupportedDataFormatException: Format \'{}\' is not ' \
               'supported.'.format(file_ext)

        if file_ext in SUPPORTED_DATA_FORMATS:
            data = None
            if file_ext == 'yaml':
                try:
                    data = yaml_load(open_and_read(file))
                except YAMLError:
                    raise YAMLError(exc1)
            elif file_ext == 'json':  # Planned
                pass
            elif file_ext == 'xml':  # Planned
                pass
            elif file_ext == 'csv':  # Planned
                pass
            self.__init__(source_data=copy(data))
            self.source_file_path = str(copy(file))
            self.source_file_data = open_and_read(file)
        elif file_ext in PLANNED_SUPPORTED_FILE_TYPES:
            raise UnsupportedFileTypeException(exc2)
        else:
            raise UnsupportedFileTypeException(exc3)

    def _load_serialized(self, data):
        self.source_data, self.source, self.data, self.dict \
            = iter_repeat(copy(data), 4)
        # self.yaml = ''  # TODO
        # self.sqlalchemy = ''  # TODO


if __name__ == '__main__':  # Testing
    # TODO: Implement CLI and use file path as follows.
    #   /Users/joeflack4/projects/pma-api/pmaapi/model/model.yaml
    try:
        model = OpenModel()
        model.load(MODEL_FILE)
        # print(model.dict)
        # print(model.yaml)
        # print(model.sqlalchemy)
    except OpenModelException as exc:
        print(exc, file=stderr)
    # pass
