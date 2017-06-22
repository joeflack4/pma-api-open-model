"""Resource class module."""


class Resource:
    """Resource class."""

    def __init__(self, resource_info):
        """Resource initialization.

        Args:
            resource_info (dict): Information about the resource.
        """
        self.name = resource_info['name']
        self.plural = resource_info['plural']

    def get(self):
        """HTTP GET method for resource.

        Returns:
            dict: The resource.

        """
        return {self.plural: ['item1', 'item2', '...']}

    @staticmethod
    def put():
        """HTTP PUT method for resource.

        Returns:
            dict: Response message.

        """
        return {"message": "Method currently unsupported."}

    @staticmethod
    def post():
        """HTTP POST method for resource.

        Returns:
            dict: Response message.

        """
        return {"message": "Method currently unsupported."}

    @staticmethod
    def delete():
        """HTTP DELETE method for resource.

        Returns:
            dict: Response message.

        """
        return {"message": "Method currently unsupported."}

    @staticmethod
    def options():
        """HTTP OPTIONS method for resource.

        Returns:
            dict: Response message.

        """
        return {"message": "Method currently unsupported."}

    @staticmethod
    def head():
        """HTTP HEAD method for resource.

        Returns:
            dict: Response message.

        """
        return {"message": "Method currently unsupported."}

    @staticmethod
    def patch():
        """HTTP PATCH method for resource.

        Returns:
            dict: Response message.

        """
        return {"message": "Method currently unsupported."}
