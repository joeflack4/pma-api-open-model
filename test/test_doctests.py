#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Doctests for package."""
from os import path as os_path


TEST_DIRECTORY = os_path.dirname(os_path.realpath(__file__))


if __name__ == '__main__':
    import doctest
    FILE = TEST_DIRECTORY + "/../" + "pmaapi/resource.py"
    doctest.testfile(filename=FILE, module_relative=False)
