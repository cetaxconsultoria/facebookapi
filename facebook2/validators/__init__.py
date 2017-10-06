import inspect

from exceptions.request import InvalidCallerError, InvalidParameterError, InvalidParameterTypeError, MissingRequiredParameterError


def validate_parameters(valid_parameters, given_parameters, func=None):
    """Validate Parameters

    Validates route parameters

    Args:
        valid_parameters (dict): Dict of dicts containing the valid parametes,
    their expected type and if they are required
        given_parameters (dict): Dict of received parametes
        func (str, optional): Caller scope name

    Raises:
        InvalidParameterError if the parameter was invalid
        InvalidParameterTypeError if the parameter type was invalid
        MissingRequiredParameterError if a required parameter is missing
    """
    func = func or inspect.currentframe().f_back.f_code.co_name

    # Check each given parameter
    for key, value in given_parameters.items():
        # If the given parameter is not valid
        if valid_parameters.get(key, None) is None:
            raise InvalidParameterError(key, value, func=func)

        # If the parameter's type is not valid
        if valid_parameters.get(key, None)['type'] != type(value):
            raise InvalidParameterTypeError(key, value, func=func)

    # For each valid parameter
    for key, value in valid_parameters.items():
        # If a required parameter is not present
        if value['required'] is True and given_parameters.get(key, None) is None:
            raise MissingRequiredParameterError(key, func)


def validate_caller(valid_callers, caller, func=None):
    """Validate Caller

    Validates route caller

    Args:
        valid_callers (dict): Dict containing the valid callers
        caller (str): Caller name

    Raises:
        InvalidCallerError if the caller was invalid
    """
    func = func or inspect.currentframe().f_back.f_code.co_name

    if valid_callers.get(caller, None) is None:
        raise InvalidCallerError(caller, func)
