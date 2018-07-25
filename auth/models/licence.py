import time
from sqlalchemy import orm

# from flask_cot.db import db


class Licence():
    id = None
    __tablename__ = 'cot_licences'
"""
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created = db.Column(db.Integer(), nullable=False, default=int(time.time()))
    modified = db.Column(db.Integer(), nullable=False, default=int(time.time()), onupdate=int(time.time()))
    master_metadata = db.Column(db.Text, nullable=True, default=None)
    description = db.Column(db.String(255), nullable=False, default=None)
    organisation_id = db.Column(db.String(36), nullable=True, default=None)
    active_status_id = db.Column(db.Integer(), nullable=False, default=0)
    _has_metadata = db.Column(db.Integer(), nullable=False, default=0)
    _archive_id = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return '<Licence %r>' % self.name

    def get_by_id(id):
        return Licence.query.first()

    @orm.reconstructor
    def init_on_load(self):
        print('After')
"""



"""
    def __init__(
        self,
        name=None,
        description=None,
        organisation_id=None,
        active_status_id=1,
        master_metadata=None
    ):
        super().__init__()
        self.id = None
        self.name = name
        self.description = description
        self.organisation_id = organisation_id
        self.active_status_id = active_status_id
        self.master_metadata = master_metadata
"""
