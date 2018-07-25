import uuid


class User(object):
    """docstring for User."""
    def __init__(self, id=None, auth_load=True):
        super(User, self).__init__()
        if id:
            self.load(id)

    def reset(self):
        self.id = None
        self.username = None
        self.email_address = None

    def load(self):
        self.id = str(uuid.uuid4())
        self.username = 'TestUsername'
        self.email_address = ''
