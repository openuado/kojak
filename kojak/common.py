import os


def is_valid_path(path):
    """To check if the path exists and if the is readable.

    @param path: The path of the file or directory
    @type path: str


    @raise IOError: If the path doesn't exists
    @raise OSError: If the path doesn't is not readable
    """
    if not os.path.exists(path):
        raise IOError("{path} is not a valid path".format(path=path))
    if not os.access(path, os.R_OK):
        raise OSError("{path} is not a readable path".format(path=path))


def pluralize(value, singular, plural=None):
    if not value:
        return singular

    if not plural:
        plural = "{singular}s".format(singular=singular)

    if isinstance(value, (list, tuple, dict)):
        value = len(value)
    elif isinstance(value, str):
        try:
            value = int(value)
        except ValueError:
            value = 1

    return singular if value == 1 else plural
