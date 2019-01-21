class Error(Exception):
    """
    An unspecified error.

    """


class MissingPermission(Error):
    """
    Missing permission when calling the API.

    """
