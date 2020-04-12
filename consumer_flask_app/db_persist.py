from datetime import datetime
from pymongo import MongoClient
import json


class Mongo:
    def __init__(self, host, port, db, collection):
        client = MongoClient(host, port)
        db = client[db]
        self.collection = db[collection]

    def insert(self, data):
        data = json.loads(data)
        assignment = {
            'data': data,
            'date': datetime.now().date().strftime('%Y-%m-%d')
        }
        result = self.collection.insert_one(assignment)
        return result.inserted_id

