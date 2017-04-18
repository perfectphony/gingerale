from pymongo import MongoClient


class Database:

    db_name = "gingerale"
    db = None

    def __init__(self, logger, host="localhost", port=27017):

        client = MongoClient(host, port)
        self.database = client[self.db_name]
        self.logger = logger

    def get(self, collection_name, class_obj, manager, id_filter=None, limit=0):
        collection = self.database[collection_name]

        id_filter = [id_filter] if type(id_filter) is int else id_filter

        documents = collection.find({"id": {"$in": id_filter}}) \
            if id_filter is not None else collection.find()

        documents.sort([("_id", -1)])

        if limit > 0:
            documents.limit(limit)

        ret = []
        for objs in documents:
            obj = class_obj(self.logger, self, manager, 0)
            for k, v in objs.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            ret.append(obj)

        return ret

