"""
connection to mongo db
"""
import os

from pymongo import MongoClient
from config import settings


class MongoDb:
    def __init__(self):
        self.connection = MongoClient(
            settings.MONGO_HOST, settings.MONGO_PORT, username=settings.MONGO_USER, password=settings.MONGO_PASS
        )
        self.database = self.connection["db-cart"]
        self.cart_collection = self.database["cart"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
