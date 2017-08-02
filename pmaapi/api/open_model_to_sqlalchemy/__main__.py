#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Open Model to SqlAlchemy"""
import yaml
from copy import copy
from pmaapi.config import MODEL_FILE


class OpenModelToSqlAlhemy:
    """Open Model to SqlAlchemy"""

    def __init__(self, file=None):
        """Initialize"""
        self.yaml, self.dict, self.sqlalchemy = None, None, None
        self.data = self.load(file, return_data=True) if file else None
        self.source_data = copy(self.data)

    def get_data(self, format):
        """Get data in specified format."""
        return self.yaml if format is 'yaml' \
            else self.dict if format in ('dict', 'dictionary') \
            else self.sqlalchemy if format is 'sqlalchemy' \
            else self.yaml

    def load(self, file, return_data=False):
        """Loads file and sets data in multiple formats.

        Side Effects:
            self.yaml (yaml): Set.
            self.dict (dict): Set.
            self.sqlalchemy (SqlAlchemy.Model): Set.

        Returns:
            yaml: If return_data.
        """
        with open(file, 'r') as stream:
            try:
                self.yaml = yaml.load(stream)
                self.dict = ''  # TODO
                self.sqlalchemy = ''  # TODO
            except yaml.YAMLError as exc:
                print(exc)

        if return_data:
            return self.yaml

if __name__ == '__main__':
    # Testing
    model = OpenModelToSqlAlhemy()
    model.load(MODEL_FILE)
    print(model.yaml, model.dict, model.sqlalchemy)
    # pass
