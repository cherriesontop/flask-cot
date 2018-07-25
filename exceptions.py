import inspect


class NotImplementedYet(Exception):
    def __init__(self, message='', errors=None):
        super().__init__(
            'NotImplementedYet in ' +
            message +
            inspect.stack()[1][3]
        )
        self.errors = errors
