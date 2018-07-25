import time
from flask_sqlalchemy import SQLAlchemy, Model
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr  # , has_inherited_table


class CotModel(Model):

    def to_dict(self):
        keys = self.__table__.columns
        offset = len(self.__tablename__) + 1
        # print('offset is ' + str(offset))
        obj = {}
        for key in keys:
            # print('key is ' + str(key))
            trimed_key = str(key)[offset:]
            # print('trimmed key is ' + trimed_key)
            obj[trimed_key] = self.__dict__[trimed_key]
        return obj

    def day_id(epoch=None):
        if epoch is None:
            epoch = time.time()

        return int(epoch // 86400)

    def month_id(epoch=None):
        if epoch is None:
            epoch = time.time()
        t = time.gmtime(epoch)
        return int((t.tm_year * 12) + t.tm_mon)

    def year_id(epoch=None):
        if epoch is None:
            epoch = time.time()
        t = time.gmtime(epoch)
        return int(t.tm_year)


db = SQLAlchemy(model_class=CotModel)
