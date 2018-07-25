from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from marshmallow import validates, ValidationError


class LeaderboardEntrySchema(Schema):
    """
        Schema for verification of externally provided values. Internal values
        such as dimentions are not verified.
    """
    id = fields.UUID(dump_only=True)

    leaderboard_id = fields.UUID(
        required=True,
        error_messages={
            'invalid_uuid': 'Not a valid UUID:#:112:#:errors?#error_112'
        }
    )
    display_name = fields.Str(
        required=True,
    )

    # user_id = fields.Str(dump_only=True)
    display_name = fields.Str(dump_only=True)
    display_avatar = fields.Str(dump_only=True)
    score_a = fields.Integer(required=True)
    score_b = fields.Integer(dump_only=True)
    position = fields.Integer(dump_only=True)
    created = fields.Integer(dump_only=True)
    selected = fields.Boolean(dump_only=True)

    class Meta:
        type_ = 'leaderboardentry'
        # self_view = 'auth.index'
        self_view_kwargs = {}
        strict = True

    """ Validators """
    @validates('display_name')
    def validate_display_name(self, dn):
        pass
        # if not licence:
        #     raise ValidationError('Unknown licence_id:#:121:#:auth?#error_121')
        # if licence['expired']:
        #     raise ValidationError(
        #         'Expired licence_id:#:122:#:auth?#error_122'
        #     )

    # @validates('augxp_version')
    # def validate_augxp_version(self, axp_v):
    #    version = get_augxp_version(axp_v)
    #    if not version:
    #        raise ValidationError('Invalid augxp_version:#:124:#:auth?#error_124')
    #    if version['upgrade_required']:
    #        raise ValidationError('Application update required:#:123:#:auth?#error_123')
