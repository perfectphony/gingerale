from pymongo import MongoClient
from datetime import datetime


class Database:
    db_name = "gingerale"

    def __init__(self, logger, host="localhost", port=27017):
        self.client = MongoClient(host, port)
        self.database = self.client[self.db_name]
        self.logger = logger

    def _get_next_id(self, collection_name):
        collection = self.database["idcounters"]
        ret = collection.find_and_modify(
            query={"_id": collection_name},
            update={"$inc": {"id": 1}},
            upsert=True,
            new=True
        )
        return ret["id"]

    def close(self):
        self.client.close()

    def delete(self, collection_name, id_list):
        #soft delete, updates delete_timestamp if not yet deleted
        id_list = [id_list] if type(id_list) is int else id_list

        collection = self.database[collection_name]

        ret = collection.update(
            {"id": {"$in": id_list}, "delete_timestamp": None},
            {"$set": {"delete_timestamp": datetime.utcnow()}},
            upsert=False
        )["nModified"]

        return {"deleted": ret}

    def set(self, collection_name, obj):
        collection = self.database[collection_name]

        if obj.id is None:
            obj.create_timestamp = datetime.utcnow()

            # get next id increment
            obj.id = self._get_next_id(collection_name)
            ret = {"inserted": collection.insert(obj.to_dict())["nInserted"]}
        else:
            ret = {"updated": collection.update(
                {"id":  obj.id},
                {"$set": obj.to_dict(False)},
                upsert=False
            )["nModified"]}

        return ret

    def get(self, collection_name, class_obj, manager, id_list=None, limit=0, show_inactive=True, show_deleted=False):
        collection = self.database[collection_name]

        id_list = [id_list] if type(id_list) is int else id_list

        query = {}

        if id_list is not None:
            query["id"] = {"$in": id_list}

        if not show_deleted:
            query["delete_timestamp"] = None

        if not show_inactive:
            query["status"] = "active"  # users that are active
            query["expiration"] = {"$lt": datetime.utcnow()}  # polls that havent expired
            query["winner_user_id"] = None  # prizes that dont have a winner

        documents = collection.find(query)
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

    def bid_prize(self, prize_id, user_id, tokens):
        # returns None if prize NOT yet won
        # returns number of tokens overpaid if won

        collection = self.database["prizes"]

        prize = collection.find_one_and_update({
                "id": prize_id,
                "$where": "this.required_bids > this.current_bid_count"
            },
            {
                "$inc": {"current_bid_count": tokens},
            },
            return_document=True
        )

        if prize is None or prize["current_bid_count"] < prize["required_bids"]:
            return None

        return prize["current_bid_count"] - prize["required_bids"]

    def get_vote_by_poll_and_user(self, user_id, poll_id):
        # returns the poll choice, False if vote not found

        collection = self.database["votes"]
        vote = collection.find({"user_id": user_id, "poll_id": poll_id})

        return None if vote is None else vote["choice"]
