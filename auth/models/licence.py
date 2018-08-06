import time
import json
from sqlalchemy import orm
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from flask_cot.db.mixins import TimestampMixin, CRUDMixin
from flask_cot.db import db
from flask_cot.core.models import BaseModel


class LicenceDb(TimestampMixin, CRUDMixin, db.Model):
    def __init__(self):
        super(LicenceDb, self).__init__()

    __tablename__ = 'cot_licences'
    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    master_metadata = db.Column(db.TEXT, nullable=True)
    description = db.Column(db.VARCHAR(255), nullable=False)
    organisation_id = db.Column(db.CHAR(36), nullable=False)
    _active_status_id = db.Column(db.Integer(), nullable=True)
    _cot_has_metadata = db.Column(db.Integer(), nullable=True)
    _cot_archive_id = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        return '<Licence id=%r name=%r desc=%r>' %\
            self.id, self.name, self.description


class Licence(BaseModel):
    def __init__(self, id=None):
        super(Licence, self).__init__()
        self._db_model = LicenceDb
        self.reset()
        if id:
            self.load(id)
            print('loaded licence ' + str(id))

    def requires_location(self):
        if self.id.startswith('1'):
            return True
        else:
            return False

    def is_active(self):
        if 1 == self.data['_active_status_id']:
            return True
        else:
            return False
