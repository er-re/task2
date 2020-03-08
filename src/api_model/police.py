from flask_restplus import fields

from server.instance import server

api = server.api

police = api.model('police', {
    'name': fields.String(required=True, description='officer full name'),
    'off': fields.Boolean(description='officer availability', default=False)
})
