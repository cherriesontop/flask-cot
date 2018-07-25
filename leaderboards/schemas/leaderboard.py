from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
# from marshmallow import validates, ValidationError


class LeaderboardSchema(Schema):
    """
        Schema for verification of externally provided values. Internal values
        such as dimentions are not verified.
    """
    id = fields.UUID(dump_only=True)
    # organisation_id = fields.UUID(dump_only=True)
    # owner_id = fields.UUID(dump_only=True)
    name = fields.Str(dump_only=True)
    experience_id = fields.UUID(dump_only=True)
    experience_name = fields.Str(dump_only=True)
    _dim_1_description = fields.Str(dump_only=True)
    _dim_2_description = fields.Str(dump_only=True)
    _dim_3_description = fields.Str(dump_only=True)
    _dim_4_description = fields.Str(dump_only=True)
    _dim_5_description = fields.Str(dump_only=True)


    class Meta:
        type_ = 'leaderboard'
        # self_view = 'auth.index'
        self_view_kwargs = {}
        strict = True
