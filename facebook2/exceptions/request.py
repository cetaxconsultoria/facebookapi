"""Request Exceptions

Exceptions that define the API request behaviour
"""

import inspect

from . import APIBaseError


class InvalidCallerError(APIBaseError):
    """Invalid caller id for a given route"""

    def __init__(self, caller, func=None):
        func = func or inspect.currentframe().f_back.f_code.co_name
        self.message = "{} is not a valid caller for the route {}".format(caller, func)
        super().__init__(self.message)


class InvalidParameterError(APIBaseError):
    """Invalid parameter key for a given route"""

    def __init__(self, key, value, func=None):
        func = func or inspect.currentframe().f_back.f_code.co_name
        self.message = "{}:{} is not a valid parameter for the route {}".format(key, value, func)
        super().__init__(self.message)


class InvalidParameterTypeError(APIBaseError):
    """Invalid parameter value for a given route"""

    def __init__(self, key, value, func=None):
        func = func or inspect.currentframe().f_back.f_code.co_name
        self.message = "{} is not a valid type for the parameter {} for the route {}".format(type(value), key, func)
        super().__init__(self.message)


class MissingRequiredParameterError(APIBaseError):
    """Invalid parameter value for a given route"""

    def __init__(self, key, func=None):
        func = func or inspect.currentframe().f_back.f_code.co_name
        self.message = "The required parameter {} is missing for the route {}".format(key, func)
        super().__init__(self.message)
