from pymongo import MongoClient


class Database:

    db_name = "gingerale"
    db = None

    def __init__(self, host, port):

        client = MongoClient(host, port)
        self.db = client[self.db_name]

