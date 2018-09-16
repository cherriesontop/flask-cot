import json
import sys
from flask import current_app
import inspect

cot_models_db_models = {}


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

    def _get_db_model(self, abstract_class):
        """ creates and caches a parent of the sqlalchemy db model with a 
            dynamic table name based on the prefix set in config
        """
        final_cls_name = abstract_class.__name__ + 'Cot'
        if final_cls_name in cot_models_db_models:
            return cot_models_db_models[final_cls_name]
        else:
            if 'COT_DATABASE_TABLE_PREFIX' in current_app.config:
                prefix = current_app.config['COT_DATABASE_TABLE_PREFIX'] + '_'
            else:
                prefix = ''
            cot_models_db_models[final_cls_name] = type(
                final_cls_name,
                (abstract_class,),
                {
                    '__tablename__': prefix + abstract_class.__base_tablename__
                }
                )
            return cot_models_db_models[final_cls_name]
