from sqlalchemy import and_

from db_model.bike import Bike
from db_model.police import Police


def assign():
    polices = Police.query.filter(and_(Police.bike_id.is_(None), Police.off.is_(False)))
    bikes = Bike.query.filter(and_(Bike.police_id.is_(None), Bike.resolved.is_(False)))
    for police, bike in zip(polices, bikes):
        police.bike_id = bike.id
        bike.police_id = police.id

