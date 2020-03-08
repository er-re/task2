from flask import Flask, request
from flask_restplus import Resource, fields
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.instance import server
from db_model.police import Police as PoliceClass
from schema.police import police_schema, polices_schema
from core.police import remove_police, re_enable_police
from api_model.police import police as police_model

api, db = server.api, server.db

police = api.namespace('police', description='officers information', path='/')


@police.route("/polices")
class Police(Resource):

    @police.param('off', type='boolean')
    def get(self):
        try:
            args = request.args
            error = police_schema.validate(args, partial=True)
            if error:
                raise ValidationError(error)
            args = dict(args)
            query = PoliceClass.query
            for attr, value in args.items():
                query = query.filter(getattr(PoliceClass, attr) == value)
            polices = query.all()
            polices = polices_schema.dump(polices)
            return {'date': polices}
        except ValidationError as err:
            return err.messages, 400
        except IntegrityError:
            return {"message": "Failure"}, 400

    @police.doc(body=police_model, responses={201: 'Success, officer was created', 400: 'Failure'})
    def post(self):
        json_data = request.get_json()
        try:
            is_added = police_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        if is_added:
            return {"message": "Success, officer was created"}, 201
        else:
            return {"message": "Failure"}, 400


@police.route("/police/<int:id>")
class Police(Resource):

    @police.doc(responses={200: ('Success', police_model), 400: 'Failure, officer could not be found'})
    def get(self, id):
        try:
            police = PoliceClass.query.get(id)
        except IntegrityError:
            return {"message": "Failure"}, 400
        police = police_schema.dump(police)
        return {"data": police}

    def patch(self, id):
        if re_enable_police(id):
            return {"message": "Success, officer was re_enabled"}
        else:
            return {"message": "Failure"}, 400

    @police.doc(responses={200: 'Success, officer was tagged as unavailable employee', 400: 'Failure'})
    def delete(self, id):
        if remove_police(id):
            return {"message": "Success, officer become off"}
        else:
            return {"message": "Failure"}, 400


