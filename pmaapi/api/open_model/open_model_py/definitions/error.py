"""Error classes."""


class OpenModelException(Exception):
    """General Exception."""
    pass


class UnexpectedException(OpenModelException):
    """For exceptions that are unknown unknowns."""
    pass


class UnsupportedFileTypeException(OpenModelException):
    """If file type is unsupported."""
    pass


class UnimplementedFunctionalityException(OpenModelException):
    """If functionality is not yet implemented."""
    pass
