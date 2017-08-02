"""Error classes."""


class OpenModelException(Exception):
    """General Exception."""
    pass


class UnexpectedException(OpenModelException):
    """General Exception."""
    pass


class UnsupportedFileTypeException(OpenModelException):
    """General Exception."""
    pass
