"""Module for resource."""
import os
from pmaapi.resource import Resource


MODULE_NAME = os.path.basename(__file__)[:-3]
RESOURCE_INFO = {
    'name': MODULE_NAME[:-1],
    'plural': MODULE_NAME
}
RESOURCE = Resource(RESOURCE_INFO)


def get():
    """HTTP GET method for resource.

    Returns:
        dict: The resource.

    """
    return RESOURCE.get()


def put():
    """HTTP PUT method for resource.

    Returns:
        dict: Response message.

    """
    return RESOURCE.put()


def post():
    """HTTP POST method for resource.

    Returns:
        dict: Response message.

    """
    return RESOURCE.post()


def delete():
    """HTTP DELETE method for resource.

    Returns:
        dict: Response message.

    """
    return RESOURCE.delete()


def options():
    """HTTP OPTIONS method for resource.

    Returns:
        dict: Response message.

    """
    return RESOURCE.options()


def head():
    """HTTP HEAD method for resource.

    Returns:
        dict: Response message.

    """
    return RESOURCE.head()


def patch():
    """HTTP PATCH method for resource.

    Returns:
        dict: Response message.

    """
    return RESOURCE.patch()
