from server.instance import server

db = server.db


class Police(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    bike_id = db.Column(db.Integer, db.ForeignKey('bike.id'), nullable=True)
    off = db.Column(db.Boolean, default=False)

