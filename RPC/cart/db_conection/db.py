"""
connection to mongo db
"""
import os

from pymongo import MongoClient
from dotenv import load_dotenv


class MongoDb:
    def __init__(self):
        load_dotenv()
        self.connection = MongoClient(
            os.getenv("MONGO_HOST"), username=os.getenv("MONGO_USER"), password=os.getenv("MONGO_PASS")
        )
        self.database = self.connection[os.getenv("MONGO_DB")]
        self.cart_collection = self.database["cart"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
