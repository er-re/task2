from flask_restplus import fields

from server.instance import server


api = server.api

bike = api.model('bike', {
    'owner': fields.String(required=True, description='bike owner'),
    'license_number': fields.Integer(required=True, description='bike license number', example='75682143'),
    'color': fields.String(description='bike color'),
    'bike_type': fields.String(enum=['Road', 'Touring', 'Mountain', 'TimeTrial', 'Hybrid', 'Other'], description='bike type'),
    'theft_date': fields.Date(dt_format='iso8601', description='The date of the robbery', example="2020-01-01"),
})

