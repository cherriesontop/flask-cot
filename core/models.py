

class BaseModel():

    def __init__(self):
        print('Base Init')
        self._db_model = None

    def reset(self):
        self._id = None
        self.data = {}

    def load(self, id):
        self.reset()
        obj = self._db_model.get_by_id(id)
        if obj:
            self._id = id
            self.data = obj.to_dict()
            return True
        else:
            return None
