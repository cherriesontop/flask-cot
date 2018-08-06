import inspect
import logging


class CotException(Exception):
    """
    Base exception for all Cot Exceptions
    """
    def __init__(self, message='', errors=None, log_level=logging.NOTSET):
        super().__init__(
            message 
        )
        self.errors = errors


class NotImplementedYet(Exception):
    def __init__(self, message='', errors=None, log_level=logging.ERROR):
        super().__init__(
            'NotImplementedYet in ' +
            message +
            inspect.stack()[1][3]
        )
        self.errors = errors
