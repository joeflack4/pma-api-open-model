"""Error classes."""


class PmaApiException(Exception):
    """General Exception."""
    pass


class DatabaseException(PmaApiException):
    """If a database error occurred."""
    pass


def raise_database_exception(_db, msg):
    """Handle database exception.

    Args:
        _db (SqlAlchemy): SqlAlchemy DB object.
        msg (str): Error message to print.

    Raises:
        DatabaseException
    """
    _db.session.rollback()
    raise DatabaseException(msg)
