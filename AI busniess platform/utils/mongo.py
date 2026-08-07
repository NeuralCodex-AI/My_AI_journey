from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config import MONGODB_URI, DATABASE_NAME


class MongoDB:

    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DATABASE_NAME]

    def collection(self, name):
        return self.db[name]

    def insert_one(self, collection, data):
        try:
            result = self.collection(collection).insert_one(data)
            return result.inserted_id
        except PyMongoError:
            return None

    def find_one(self, collection, query):
        return self.collection(collection).find_one(query)

    def find(self, collection, query=None):
        if query is None:
            query = {}
        return list(self.collection(collection).find(query))

    def update_one(self, collection, query, data):
        return self.collection(collection).update_one(
            query,
            {"$set": data}
        )

    def delete_one(self, collection, query):
        return self.collection(collection).delete_one(query)

    def delete_many(self, collection, query):
        return self.collection(collection).delete_many(query)