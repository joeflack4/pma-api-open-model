"""Error classes."""


class OpenModelException(Exception):
    """General Exception."""
    pass


class UnexpectedDataTypeException(OpenModelException):
    """If data type was unexpected."""
    pass


class UnsupportedFileTypeException(OpenModelException):
    """If file type is unsupported."""
    pass


class UnimplementedFunctionalityException(OpenModelException):
    """If functionality is not yet implemented."""
    pass


class InvalidSchemaException(OpenModelException):
    """If there is an error when trying to read the data model."""
    pass
