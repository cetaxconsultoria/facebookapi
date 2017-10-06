""" Exceptions

Various custom exceptions that define the application errors
"""


class Error(Exception):
    """Generic base error"""
    pass


class APIBaseError(Error):
    """Base API exception"""
    pass
