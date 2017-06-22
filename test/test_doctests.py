"""Doctests for package."""
from os import path as os_path


TEST_DIRECTORY = os_path.dirname(os_path.realpath(__file__))


if __name__ == '__main__':
    import doctest
    file = TEST_DIRECTORY + "/../" + "pmaapi/resource.py"
    doctest.testfile(filename=file, module_relative=False)
