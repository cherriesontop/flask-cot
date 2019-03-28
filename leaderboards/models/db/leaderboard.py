from sqlalchemy import orm

from flask_cot.db import db
from flask_cot.db.mixins import TimestampMixin, CRUDMixin


class LeaderboardDb(TimestampMixin, CRUDMixin, db.Model):
    """docstring for Leaderboard."""

    __abstract__ = True
    __base_tablename__ = 'leaderboards'
    id = db.Column(db.CHAR(36), nullable=False, primary_key=True)
    organisation_id = db.Column(db.CHAR(36), nullable=True)
    owner_id = db.Column(db.CHAR(36), nullable=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    _dim_1_description = db.Column(db.VARCHAR(255), nullable=True)
    _dim_2_description = db.Column(db.VARCHAR(255), nullable=True)
    _dim_3_description = db.Column(db.VARCHAR(255), nullable=True)
    _dim_4_description = db.Column(db.VARCHAR(255), nullable=True)
    _dim_5_description = db.Column(db.VARCHAR(255), nullable=True)
    _pref_multi_entry = db.Column(db.SmallInteger(), default=0)
    _pref_anon_entry = db.Column(db.SmallInteger(), default=0)
    _pref_score_col = db.Column(db.SmallInteger(), default=0)
    _pref_score_a_direction = db.Column(db.VARCHAR(45), default='DESC')
    _pref_score_b_direction = db.Column(db.VARCHAR(45), default='DESC')
    _pref_created_direction = db.Column(db.VARCHAR(45), default='ASC')

    def __repr__(self):
        return '<Leaderboard %r>' % self.name

    @orm.reconstructor
    def init_on_load(self):
        pass
