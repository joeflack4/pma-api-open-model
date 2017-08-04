"""Config"""
# from pathlib import PurePath  # - Disabled: Not supported in Python 2.
import os


PACKAGE_ROOT = os.path.dirname(__file__)
MODEL_FILE = PACKAGE_ROOT + '/model/model.yaml'
PLANNED_SUPPORTED_FILE_TYPES = ('csv', 'json', 'xml')
SUPPORTED_DATA_FORMATS = ('yaml',)
SUPPORTED_DATA_TYPES = (str, bytes, int)  # - Disabled: pathlib.PurePath
