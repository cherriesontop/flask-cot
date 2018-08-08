# from sqlalchemy import orm, ForeignKey
from sqlalchemy import and_, text
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from flask_cot.db.mixins import TimestampMixin, CRUDMixin
from flask_cot.db import db
from flask_cot.core.models import BaseModel

# from augxpapi.core.models.access_code import AccessCodeDb


class LicenceLocationSchema(Schema):
    """
        Schema for verification of externally provided values. Internal values
        are not verified.
    """
    id = fields.UUID(dump_only=True)
    licence_id = fields.UUID(dump_only=True)
    lat_tl = fields.Decimal(places=6, as_string=False, dump_only=True)
    long_tl = fields.Decimal(places=6, as_string=False, dump_only=True)
    lat_br = fields.Decimal(places=6, as_string=False, dump_only=True)
    long_br = fields.Decimal(places=6, as_string=False, dump_only=True)
    _active_status_id = fields.Integer(dump_only=True)

    class Meta:
        type_ = 'licence_location'
        # self_view = 'auth.index'
        self_view_kwargs = {}
        strict = True


class LicenceLocationDb(TimestampMixin, CRUDMixin, db.Model):
    def __init__(self):
        super(LicenceLocationDb, self).__init__()

    __tablename__ = 'cot_licence_locations'
    id = db.Column(db.CHAR(36), primary_key=True)
    licence_id = db.Column(db.CHAR(36))  # , ForeignKey(AccessCodeDb.id))
    lat_tl = db.Column(db.DECIMAL(precision=9, scale=6))
    long_tl = db.Column(db.DECIMAL(precision=9, scale=6))
    lat_br = db.Column(db.DECIMAL(precision=9, scale=6))
    long_br = db.Column(db.DECIMAL(precision=9, scale=6))
    _active_status_id = db.Column(db.INTEGER(), nullable=True)

    def __repr__(self):
        return '<LicenceLocation id=%r>' % self.id


class LicenceLocation(BaseModel):
    def __init__(self, id=None):
        super(LicenceLocation, self).__init__()
        self._db_model = LicenceLocationDb
        self.reset()
        if id:
            self.load(id)


class LicenceLocations(BaseModel):
    def __init__(self):
        super(LicenceLocations, self).__init__()
        self._db_model = LicenceLocationDb
        self.reset()

    def within_geofence(self, licence_id, loc_lat, loc_long, mode='simple'):
        filter_group = []
        filter_group.append(
            text("licence_id='"+str(licence_id)+"'")
        )
        filter_group.append(
            text("lat_tl>='"+str(loc_lat)+"'")
        )
        filter_group.append(
            text("lat_br<='"+str(loc_lat)+"'")
        )
        filter_group.append(
            text("long_tl<='"+str(loc_long)+"'")
        )
        filter_group.append(
            text("long_br>='"+str(loc_long)+"'")
        )
        obj = self._db_model.query.filter(
                and_(*filter_group)
            ).first()

        return obj
