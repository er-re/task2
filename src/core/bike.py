from sqlalchemy import exc
from contextlib import contextmanager

from server.instance import server
from db_model.bike import Bike
from db_model.police import Police
from core.assign import assign

db = server.db


@contextmanager
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


@contextmanager
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
