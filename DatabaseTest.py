import random

class Database:
    db_name = "gingerale"

    def __init__(self, logger, host="localhost", port=27017):
        self.logger = logger
        self.lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eget dui erat. In augue ligula, fringilla vitae fringilla eu, dapibus eu massa. Donec ut suscipit urna, quis pharetra sapien. Donec lobortis lectus eget neque suscipit, at ornare arcu venenatis. Curabitur eget dui arcu. Nulla ut neque vel ipsum pellentesque luctus at et nulla. Sed orci diam, vulputate sit amet fringilla id, tempor in lacus. Maecenas scelerisque aliquet orci, feugiat volutpat urna commodo eu.".split(" ")

    def _get_next_id(self, collection_name):
        pass

    def close(self):
        pass

    def delete(self, collection_name, id_list):
        return {"deleted": 0}

    def set(self, collection_name, obj):
        return {"updated": 0}

    def get(self, collection_name, class_obj, manager, id_list=None, limit=0, show_inactive=True, show_deleted=False):
        ret = []
        for i in range(limit, 0, -1):
            obj = class_obj(self.logger, self, manager)
            for k, v in obj.__dict__.items():
                if k == "id":
                    v = i

                setattr(obj, k, v)
            ret.append(obj)

        return ret

    def bid_prize(self, prize_id, user_id, tokens):
        pass

    def get_vote_by_poll_and_user(self, user_id, poll_id):
        pass
