from sys import argv
import json
from time import sleep
from urllib.parse import urlparse, parse_qs

from DatabaseMongoDB import Database
from LoggerNone import Logger

from Poll import *
from User import *
from Prize import *


class GingerAle:
    def __init__(self, http_path):
        self.logger = Logger()
        self.db = Database(self.logger)

        self.user_manager = UserManager(self.logger, self.db)
        self.prize_manager = PrizeManager(self.logger, self.db, self.user_manager)
        self.poll_manager = PollManager(self.logger, self.db, self.prize_manager, self.user_manager)

        parsed_url = urlparse(http_path)
        parsed_query = parse_qs(parsed_url.query)

        args = json.loads(parsed_query["args"][0])
        method = "http_" + parsed_url.path[1:]

        ret = json.dumps(
            self.__getattribute__(method)(args),
            sort_keys=False,
            indent=4,
            separators=(',', ': '),
            default=lambda obj: obj.isoformat('T') if type(obj) is datetime else None,
            skipkeys=True
        )

        print(ret)

    def _get(self, args, manager):
        show_deleted = True if ("show_deleted" in args and args["show_deleted"]) else False
        show_details = True if ("show_details" in args and args["show_details"]) else False
        limit = args["limit"] if "limit" in args else 0
        id_filter = args["id"] if "id" in args else None
        objs = manager.get(id_filter, limit, show_deleted)
        return [obj.to_dict() for obj in objs]

    def _set(self, args, manager, obj_class):
        obj = obj_class(self.logger, self.db, manager)
        for k, v in args.items():
            obj.__setattr__(k, v)
        return obj.set()

    def _delete(self, args, manager):
        id_list = args["id"] if "id" in args else None
        return manager.delete(id_list)

    def http_test(self, args):
        sleep(10)
        return {}

    def http_polls(self, args):
        return self._get(args, self.poll_manager)

    def http_set(self, args):
        return self._set(args, self.poll_manager, Poll)

    def http_del(self, args):
        return self._delete(args, self.poll_manager)

    def http_prizes(self, args):
        return self._get(args, self.prize_manager)

    def http_prize_set(self, args):
        return self._set(args, self.prize_manager, Prize)

    def http_prize_del(self, args):
        return self._delete(args, self.prize_manager)

    def http_users(self, args):
        return self._get(args, self.user_manager)

    def http_user_set(self, args):
        return self._set(args, self.user_manager, User)

    def http_user_del(self, args):
        return self._delete(args, self.user_manager)

    def http_poll_vote(self, args):
        user_id = args["user_id"],
        poll_id = args["poll_id"],
        option = args["option"],

        user = self.user_manager.get(user_id)
        poll = self.poll_manager.get(poll_id)

        if user is None:
            return {"vote": False, "reason": GC.INVALID_USER}

        if poll is None:
            return {"vote": False, "reason": GC.INVALID_POLL}

        return poll.vote(user, option)

    def http_prize_bid(self, args):
        user_id = args["user_id"],
        prize_id = args["prize_id"],
        tokens = args["tokens"],

        user = self.user_manager.get(user_id)
        prize = self.prize_manager.get(prize_id)

        if user is None:
            return {"bid": False, "reason": GC.INVALID_USER}

        if prize is None:
            return {"bid": False, "reason": GC.INVALID_PRIZE}

        return prize.bid(user, tokens)


if __name__ == "__main__":
    GingerAle(argv[1])
