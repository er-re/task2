from sqlalchemy import exc

from server.instance import server
from db_model.bike import Bike
from db_model.police import Police
from core.assign import assign

db = server.db


def add_police(**data):
    try:
        police = Police(**data)
        db.session.add(police)
        assign()
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False


def remove_police(id):
    try:
        police = Police.query.filter_by(id=id).first()
        police.off = True
        police.bike_id = None
        bike = Bike.query.filter_by(police_id=id, resolved=False).first()
        if bike:
            bike.police_id = None
        assign()
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False


def re_enable_police(id):
    try:
        police = Police.query.filter_by(id=id).first()
        police.off = False
        assign()
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False
