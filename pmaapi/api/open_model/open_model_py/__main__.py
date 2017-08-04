#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Open Model to SqlAlchemy"""
from sys import stderr
from os.path import isfile
from copy import copy
from itertools import repeat as iter_repeat
from yaml import load as yaml_load, YAMLError
from pmaapi.config import MODEL_FILE, SUPPORTED_FILE_TYPES, \
    PLANNED_SUPPORTED_FILE_TYPES
from pmaapi.api.open_model_py.open_model_py.definitions.error \
    import UnexpectedException, UnsupportedFileTypeException, \
    UnimplementedFunctionalityException


class OpenModel:
    """Open Model to SqlAlchemy"""

    def __init__(self, source_data=None):
        """Initialize.

        Arguments:
            source_data (dict): Source data in Python dictionary serialization.
        """
        self.data, self.source_data, self.source_file_data, \
            self.source_file_path, self.yaml, self.sqlalchemy, \
            self.open_model_version, self.config, self.info, self.models, \
            self.abstract_models, self.relations, self.custom_fields\
            = iter_repeat(None, 13)
        self.source = self.source_data
        self.dict = self.data

        if source_data:
            # if file... # TODO
            self.source_data = source_data
            self.data = copy(self.source_data)
            self.yaml, self.sqlalchemy = None, None  # TODO: Store data types.
            self.source_file_data, self.source_file_path = None, None  # TODO

            # self.dict = yaml.load(stream)
            # self.yaml = ''  # TODO
            # self.sqlalchemy = ''  # TODO

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
        """ksjflj"""
        if isfile(source_data):
            self._load_file(file=source_data)
        else:
            self._load_serialized(data=source_data)

    def _load_file(self, file):
        """Loads file, and runs initialization in Python dictionary format.

        Side Effects:
            self.__init__: Initializes with source file data.

        Raises:
            UnexpectedException, UnsupportedFileTypeException
        """
        exc1 = 'UnexpectedException: An unexpected error occurred.\n'
        exc2 = 'UnsupportedFileTypeException: Apologies, but file type \'{}\''\
               ' is not yet supported.'
        exc3 = 'UnsupportedFileTypeException: File type \'{}\' is not ' \
               'supported.'

        with open(file, 'r') as stream:
            # print(copy(stream.read()))
            self.source_file_data = str(copy(stream).read())
            # self.source_file_data.write(stream.read())

            # print(self.source_file_data)
            # print(stream)


            file_ext = stream.name.rpartition('.')[-1]
            exc2, exc3 = exc2.format(file_ext), exc3.format(file_ext)
            if file_ext in SUPPORTED_FILE_TYPES:
                data = None
                if file_ext == 'yaml':
                    try:
                        data = yaml_load(stream)
                        stream.seek(0)  # Reset cursor so can be read again.
                    except YAMLError:
                        raise UnexpectedException(exc1)
                elif file_ext == 'json':  # Planned
                    pass
                elif file_ext == 'xml':  # Planned
                    pass
                elif file_ext == 'csv':  # Planned
                    pass
                self.__init__(source_data=copy(data))
                self.source_file_path = copy(file)
                self.source_file_data = stream.read()

                # print(self.source_file_data)

            elif file_ext in PLANNED_SUPPORTED_FILE_TYPES:
                raise UnsupportedFileTypeException(exc2)
            else:
                raise UnsupportedFileTypeException(exc3)

    def _load_serialized(self, data):  # TODO
        raise UnimplementedFunctionalityException(
            'UnimplementedFunctionalityException: Loading from direct '
            'serialization data format is not yet supported. Please load from'
            'file.')


if __name__ == '__main__':  # Testing
    try:
        model = OpenModel()
        model.load(MODEL_FILE)
        print(model.dict)
        # print(model.yaml)
        # print(model.sqlalchemy)
        print(model.source_file_data)
    except Exception as exc:
        print(exc, file=stderr)
    # pass
