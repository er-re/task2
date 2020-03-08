from flask import Flask, request
from flask_restplus import Resource, fields
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.instance import server
from db_model.bike import Bike as BikeClass
from schema.bike import bike_schema, bikes_schema
from core.bike import remove_bike
from api_model.bike import bike as bike_model

api, db = server.api, server.db

bike = api.namespace('bike', description='bikes information', path='/')


@bike.route("/bikes")
class Bike(Resource):

    @bike.param('owner', type='string')
    @bike.param('license_number', type='integer')
    @bike.param('color',  type='string')
    @bike.param('bike_type', type='enum')
    @bike.param('theft_date', type='date')
    def get(self):
        try:
            args = request.args
            error = bike_schema.validate(args, partial=True)
            if error:
                raise ValidationError(error)
            args = dict(args)
            query = BikeClass.query
            for attr, value in args.items():
                query = query.filter(getattr(BikeClass, attr) == value)
            bikes = query.all()
            bikes = bikes_schema.dump(bikes)
            return {"data": bikes}
        except ValidationError as err:
            return err.messages, 400
        except IntegrityError:
            return {"message": "Failure"}, 400

    @bike.doc(body=bike_model, responses={201: 'Success, bike was created', 400: 'Failure'})
    def post(self):
        try:
            json_data = request.get_json()
            is_added = bike_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400
        if is_added:
            return {"message": "Success, bike was created"}, 201
        else:
            return {"message": "Failure"}, 400


@bike.route("/bike/<int:id>")
class Bike(Resource):

    @bike.doc(responses={200: ('Success', bike_model), 400: 'Failure'})
    def get(self, id):
        try:
            bike = BikeClass.query.get(id)
        except IntegrityError:
            return {"message": "bike could not be found."}, 400
        bike = bike_schema.dump(bike)
        return {"data": bike}

    @bike.doc(responses={200: f'Success, bike was tagged as a resolved case', 400: f'Failure'})
    def delete(self, id):
        if remove_bike(id):
            return {"message": "Success, bike was tagged as a resolved case"}
        else:
            return {"message": "Failure"}, 400


