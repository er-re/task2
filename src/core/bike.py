from sqlalchemy import exc

from server.instance import server
from db_model.bike import Bike
from db_model.police import Police
from core.assign import assign

db = server.db


def add_bike(**data):
    try:
        bike = Bike(**data)
        db.session.add(bike)
        assign()
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False


def remove_bike(id):
    try:
        bike = Bike.query.filter_by(id=id).first()
        bike.resolved = True

        police = Police.query.filter_by(bike_id=id).first()
        if police:
            police.bike_id = None
        assign()
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False
