from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields

from server.environment import environment_config


class Server(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
                       version='1.0',
                       title='Bike theft API',
                       description='An API for reporting stolen bike and assigning officer for finding them',
                       doc=environment_config["swagger-url"]
        )
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
        self.db = SQLAlchemy(self.app)
        self.ma = Marshmallow(self.app)

    def init_db(self):
        self.db.create_all()

    def run(self):
        self.app.run(
                debug=environment_config["debug"],
                port=environment_config["port"]
            )


server = Server()





