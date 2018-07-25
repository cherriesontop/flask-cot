from sqlalchemy import orm

from flask_cot.db import db
from flask_cot.db.mixins import TimestampMixin, CRUDMixin


class LeaderboardEntryDb(TimestampMixin, CRUDMixin, db.Model):
    """docstring for LeaderboardEntry."""

    __tablename__ = 'leaderboard_entries'
    id = db.Column(db.CHAR(36), nullable=False, primary_key=True)
    leaderboard_id = db.Column(db.CHAR(36), nullable=True)
    _dim_1 = db.Column(db.Integer(), nullable=True)
    _dim_2 = db.Column(db.Integer(), nullable=True)
    _dim_3 = db.Column(db.Integer(), nullable=True)
    _dim_4 = db.Column(db.VARCHAR(255), nullable=True)
    _dim_5 = db.Column(db.VARCHAR(255), nullable=True)
    user_id = db.Column(db.CHAR(36), nullable=True)
    display_name = db.Column(db.VARCHAR(255), nullable=True)
    display_avatar = db.Column(db.VARCHAR(255), nullable=True)
    score_a = db.Column(db.Integer(), nullable=False, default=0)
    score_b = db.Column(db.Integer(), nullable=False, default=0)

    def __repr__(self):
        return '<LeaderboardEntry %r %r>' % self.display_name, self.id

    @orm.reconstructor
    def init_on_load(self):
        print('After')

    def get_by_id(id):
        return LeaderboardEntryDb.query.filter_by(id=id).first()
