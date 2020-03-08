from marshmallow import fields, post_load

from server.instance import server
from core.police import add_police, remove_police

ma = server.ma


class PoliceSchema(ma.Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    bike_id = fields.Int()
    off = fields.Bool()

    @post_load
    def make_object(self, data, **kwargs):
        return True if add_police(**data) else False


police_schema = PoliceSchema()
polices_schema = PoliceSchema(many=True)