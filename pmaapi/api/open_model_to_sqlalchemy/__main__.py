#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Open Model to SqlAlchemy"""
import yaml
from sys import stderr
from copy import copy
from pmaapi.config import MODEL_FILE, SUPPORTED_FILE_TYPES
from pmaapi.api.open_model_to_sqlalchemy.definitions.error \
    import UnexpectedException, UnsupportedFileTypeException


class OpenModel:
    """Open Model to SqlAlchemy"""

    def __init__(self, file=None):
        """Initialize"""
        self.data, self.source_data = None, None
        self.yaml, self.dict, self.sqlalchemy = None, None, None
        self.open_model_version, self.config, self.info = None, None, None
        self.models, self.abstract_models, self.relations = None, None, None
        if file:
            self.source_data = file
            self.data = copy(self.source_data)
            self.dict = self.data
            self.yaml, self.sqlalchemy = None, None  # TODO

    # self.dict = yaml.load(stream)
    # self.yaml = ''  # TODO
    # self.sqlalchemy = ''  # TODO

    def __iter__(self):
        yield 'open_model', self.dict

    def __str__(self):
        return str(self.dict)

    def get_data(self, data_format):
        """Get data in specified format."""
        return self.yaml if data_format is 'yaml' \
            else self.dict if data_format in ('dict', 'dictionary') \
            else self.sqlalchemy if data_format is 'sqlalchemy' \
            else self.yaml

    def load(self, file):
        """Loads file and sets data in multiple formats.

        Side Effects:
            Initializes with source file data, setting various instance vars.

        Raises:
            OpenModelError: If not a supported file type.
            YAMLError: If something unexpected happens when loading YAML.
        """
        with open(file, 'r') as stream:
            file_extension = stream.name.rpartition('.')[-1]
            if file_extension not in SUPPORTED_FILE_TYPES:
                print(SUPPORTED_FILE_TYPES)
                msg = 'UnsupportedFileTypeException: File type \'{}\' is not '\
                      'supported.'.format(file_extension)
                raise UnsupportedFileTypeException(msg)
            try:
                self.__init__(file=yaml.load(stream))
            except yaml.YAMLError:
                msg = 'UnexpectedException: An unexpected error occurred.\n'
                raise UnexpectedException(msg)

if __name__ == '__main__':  # Testing
    try:
        model = OpenModel()
        model.load(MODEL_FILE)
        print(model.yaml, model.dict, model.sqlalchemy)
    except Exception as exc:
        print(exc, file=stderr)
    # pass
