import json


class BaseModel():

    def __init__(self):
        self._db_model = None
        self.obj = None

    def reset(self):
        self.obj = None
        self.id = None
        self.data = {}

    def load(self, id):
        self.reset()
        self.obj = self._db_model.get_by_id(id)
        if self.obj:
            self.id = id
            self.data = self.obj.to_dict()
            if "master_metadata" in self.data and self.data['master_metadata']:
                self.data['master_metadata'] =\
                    json.loads(self.data["master_metadata"])
            return True
        else:
            return None
