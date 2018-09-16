import time
from flask_cot.db import db


class CotMeta(object):
    _cot_has_metadata = db.Column(
        db.Integer(),
        default=0,
        nullable=False
    )
    _cot_archive_id = db.Column(
        db.Integer(),
        default=0,
        onupdate=0,
        nullable=False
    )


class TimestampMixin(object):
    """
    Provides the :attr:`created` and :attr:`updated` audit timestamps
    """
    # Timestamp for when this instance was created, in UTC
    created = db.Column(
        db.Integer(),
        default=time.time,
        nullable=False
    )
    # Timestamp for when this instance was last updated (via the app), in UTC
    updated = db.Column(
        db.Integer(),
        default=time.time,
        onupdate=time.time,
        nullable=False
    )


class CRUDMixin(object):
    # __table_args__ = {'extend_existing': True}

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    """
    @classmethod
    def query(cls):
        return db.session.query(cls)

    @classmethod
    def get(cls, _id):
        if any((isinstance(_id, basestring) and _id.isdigit(),
                isinstance(_id, (int, float))),):
            return cls.query.get(int(_id))
        return None

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_or_404(cls, _id):
        rv = cls.get(_id)
        if rv is None:
            abort(404)
        return rv

    @classmethod
    def get_or_create(cls, **kwargs):
        r = cls.get_by(**kwargs)
        if not r:
            r = cls(**kwargs)
            db.session.add(r)
        return r

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    """
