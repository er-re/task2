import enum
from server.instance import server

db = server.db


class BikeTypeEnum(enum.Enum):
    Road = 'Road'
    Touring = 'Touring'
    Mountain = 'Mountain'
    Hybrid = 'Hybrid'
    Other = 'Other'


class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    license_number = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(20), nullable=True)
    bike_type = db.Column(db.Enum(BikeTypeEnum), default=BikeTypeEnum.Other)
    theft_date = db.Column(db.Date(), nullable=True)

    police_id = db.Column(db.Integer, db.ForeignKey('police.id'), nullable=True)
    resolved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'owner "{self.owner}"'

