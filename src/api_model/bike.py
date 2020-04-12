from flask_restplus import fields

from server.instance import server


api = server.api

bike = api.model('bike', {
    'owner': fields.String(required=True, description='bike owner', example='Ali Kalan'),
    'phone': fields.String(required=True, description='owner phone number', example='09122222222'),
    'license_number': fields.Integer(required=True, description='bike license number', example='008462'),
    'color': fields.String(description='bike color', example='silver'),
    'bike_type': fields.String(enum=['Road', 'Touring', 'Mountain', 'TimeTrial', 'Hybrid', 'Other'], description='bike type'),
    'theft_date': fields.Date(dt_format='iso8601', description='The date of the robbery', example="2020-04-01"),
})

