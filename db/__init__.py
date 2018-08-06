import time
from flask_sqlalchemy import SQLAlchemy, Model
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr  # , has_inherited_table


class CotModel(Model):

    def to_dict(self):
        keys = self.__table__.columns
        offset = len(self.__tablename__) + 1
        objj = {}
        for key in keys:
            trimed_key = str(key)[offset:]
            objj[trimed_key] = self.__dict__[trimed_key]
        return objj

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
