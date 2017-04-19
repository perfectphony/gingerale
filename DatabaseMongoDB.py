from pymongo import MongoClient
from datetime import datetime

class Database:

    db_name = "gingerale"
    db = None

    def __init__(self, logger, host="localhost", port=27017):

        client = MongoClient(host, port)
        self.database = client[self.db_name]
        self.logger = logger

    def delete(self, collection_name, id_list):
        #soft delete
        id_list = [id_list] if type(id_list) is int else id_list

        obj_deleted = True

        try:
            collection = self.database[collection_name]

            ret = collection.update(
                {"id": {"$in": id_list}, "delete_timestamp": None},
                {"$set": {"delete_timestamp": datetime.utcnow()}},
                upsert=False
            )["nModified"]
            if ret == 0:
                obj_deleted = False
            reason = "{} deleted".format(ret)

        except Exception as ex:
            reason = ex.args[0]
            obj_deleted = False

        return {"set": obj_deleted, "reason": reason}

    def set(self, collection_name, obj):
        collection = self.database[collection_name]

        obj_updated = True
        reason = ""

        try:
            if obj.id is None:
                #gingerale is engine based, dont need to worry about concurrency
                obj.id = collection.find({"id": {"$gt": 1}}, {"id": 1, "_id": 0}).sort([("id", -1)]).limit(1)[0]["id"]+1
                collection.insert(obj.to_dict())
            else:
                ret = collection.update(
                    {"id":  obj.id},
                    {"$set": obj.to_dict(False)},
                    upsert=False
                )["nModified"]
                reason = "{} modified".format(ret)
        except Exception as ex:
            reason = ex.args[0]
            obj_updated = False

        return {"set": obj_updated, "reason": reason}

    def get(self, collection_name, class_obj, manager, id_list=None, limit=0, show_deleted=False):
        collection = self.database[collection_name]

        id_list = [id_list] if type(id_list) is int else id_list

        if show_deleted:
            documents = collection.find({
                "id": {"$in": id_list}
            }) if id_list is not None else collection.find()
        else:
            documents = collection.find({
                "id": {"$in": id_list}, "delete_timestamp": None
            }) if id_list is not None else collection.find({"delete_timestamp": None})

        documents.sort([("id", -1)])

        if limit > 0:
            documents.limit(limit)

        ret = []
        for objs in documents:
            obj = class_obj(self.logger, self, manager)
            for k, v in objs.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)

            ret.append(obj)

        return ret

