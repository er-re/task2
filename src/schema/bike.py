from marshmallow import fields, post_load, pre_load,  ValidationError

from server.instance import server
from db_model.bike import BikeTypeEnum
from core.bike import add_bike


ma = server.ma


def validate_type(bike_type):
    if bike_type not in [attr for attr in BikeTypeEnum.__dict__.keys() if attr[:1] != '_']:
        raise ValidationError("bike type must be one of the listed choice")


class BikeSchema(ma.Schema):
    id = fields.Int()
    owner = fields.Str(required=True)
    phone = fields.Str(required=True)
    license_number = fields.Int(required=True)
    color = fields.Str()
    bike_type = fields.Str(validate=validate_type)
    theft_date = fields.Date()

    police_id = fields.Int()
    resolved = fields.Bool()

    @post_load
    def make_object(self, data, **kwargs):
        return True if add_bike(**data) else False


bike_schema = BikeSchema()
bikes_schema = BikeSchema(many=True)