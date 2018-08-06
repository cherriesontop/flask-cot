from flask_cot.exceptions import CotException
import logging
"""

All COT exceptions cocerned with the Auth module functionality


"""


class AuthException(CotException):
    """
    Base exception for all Auth Exceptions
    """
    def __init__(self, message='', errors=None, log_level=logging.NOTSET):
        super().__init__(
            message,
            errors
        )


class LicenceException(AuthException):
    """
    Base exception for all Licence Exceptions
    """
    def __init__(self, message='', errors=None, log_level=logging.NOTSET):
        super().__init__(
            message,
            errors
        )


class LicenceNotFoundException(LicenceException):
    def __init__(self, message='', errors=None, log_level=logging.WARNING):
        super().__init__(
            message,
            errors
        )


class LicenceNotActiveException(LicenceException):
    def __init__(self, message='', errors=None, log_level=logging.INFO):
        super().__init__(
            message,
            errors
        )


class UserException(AuthException):
    """
    Base exception for all User Exceptions
    """
    def __init__(self, message='', errors=None, log_level=logging.NOTSET):
        super().__init__(
            message,
            errors
        )
