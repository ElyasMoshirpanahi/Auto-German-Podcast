from pymongo import MongoClient
from pymongo.server_api import ServerApi
from src.config import MONGODB_URI

class Database:
    def __init__(self):
        if not MONGODB_URI:
            print("Warning: MONGODB_URI is not set. Database operations will fail.")
            self.collection = None
            return
            
        self.client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
        self.db = self.client['podcast']
        self.collection = self.db.titles

    def exists(self, title):
        if self.collection is None: return False
        return self.collection.find_one({"title": title, "status": {"$in": ["posted", "broken"]}}) is not None

    def add(self, title, url, status="posted", log=None):
        if self.collection is None: return
        data = {"title": title, "url": url, "status": status}
        if log:
            data["log"] = log
        self.collection.insert_one(data)
