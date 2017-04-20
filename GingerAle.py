from sys import argv
import json
from datetime import datetime
from time import sleep
from urllib.parse import urlparse, parse_qs

from DatabaseMongoDB import Database
from LoggerNone import Logger

from Poll import PollManager
from User import UserManager
from Prize import PrizeManager
from PollComment import PollCommentManager
from PrizeComment import PrizeCommentManager
from PrizeBid import PrizeBidManager
from PollVote import PollVoteManager


class GingerAle:
    def __init__(self, http_path):
        self.logger = Logger()
        self.db = Database(self.logger)
        self.user_manager = UserManager(self.logger, self.db)
        self.prize_manager = PrizeManager(self.logger, self.db)
        self.poll_manager = PollManager(self.logger, self.db)
        self.pollvote_manager = PollVoteManager(self.logger, self.db)
        self.prizebid_manager = PrizeBidManager(self.logger, self.db)
        self.pollcomment_manager = PollCommentManager(self.logger, self.db)
        self.prizecomment_manager = PrizeCommentManager(self.logger, self.db)

        parsed_url = urlparse(http_path)
        parsed_query = parse_qs(parsed_url.query)

        args = json.loads(parsed_query["args"][0]) if "args" in parsed_query else {}
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

        self.db.close()
        self.logger.close()

    def _get_objs(self, args, manager):
        show_deleted = True if ("show_deleted" in args and args["show_deleted"]) else False
        show_details = True if ("show_details" in args and args["show_details"]) else False
        limit = args["limit"] if "limit" in args else 0
        id_list = args["id"] if "id" in args else None
        objs = manager.get(id_list, limit, show_deleted=show_deleted)
        return [obj.to_dict() for obj in objs]

    def _fill_new_obj(self, args, manager):
        obj = manager.obj_class(self.logger, self.db, manager)
        for k, v in args.items():
            obj.__setattr__(k, v)
        return obj

    def _set_obj(self, args, manager):
        return self._fill_new_obj(args, manager).set()

    def _delete_objs(self, args, manager):
        id_list = args["id"] if "id" in args else None
        return manager.delete(id_list)

    def http_test(self, args):
        sleep(10)
        return {}

    # region std http calls
    def http_polls(self, args):
        return self._get_objs(args, self.poll_manager)

    def http_poll_set(self, args):
        return self._set_obj(args, self.poll_manager)

    def http_polls_del(self, args):
        return self._delete_objs(args, self.poll_manager)

    def http_prizes(self, args):
        return self._get_objs(args, self.prize_manager)

    def http_prize_set(self, args):
        return self._set_obj(args, self.prize_manager)

    def http_prizes_del(self, args):
        return self._delete_objs(args, self.prize_manager)

    def http_users(self, args):
        return self._get_objs(args, self.user_manager)

    def http_user_set(self, args):
        return self._set_obj(args, self.user_manager)

    def http_users_del(self, args):
        return self._delete_objs(args, self.user_manager)

    def http_pollvotes(self, args):
        return self._get_objs(args, self.pollvote_manager)

    def http_pollvote_set(self, args):
        return self._set_obj(args, self.pollvote_manager)

    def http_pollvotes_del(self, args):
        return self._delete_objs(args, self.pollvote_manager)

    def http_prizebids(self, args):
        return self._get_objs(args, self.prizebid_manager)

    def http_prizebid_set(self, args):
        return self._set_obj(args, self.prizebid_manager)

    def http_prizebids_del(self, args):
        return self._delete_objs(args, self.prizebid_manager)

    def http_comments(self, args):
        return self._get_objs(args, self.comment_manager)

    def http_comment_set(self, args):
        return self._set_obj(args, self.comment_manager)

    def http_comments_del(self, args):
        return self._delete_objs(args, self.comment_manager)

    # endregion

    def http_user_vote_poll(self, args):
        user_id = args["user_id"] if "user_id" in args else None
        poll_id = args["poll_id"] if "poll_id" in args else None

        users = self.user_manager.get(user_id, 1, show_inactive=False)
        user = users[0] if len(users) > 0 else None

        polls = self.poll_manager.get(poll_id, 1, show_inactive=False)
        poll = polls[0] if len(polls) > 0 else None

        return poll.vote(user, self._fill_new_obj(args, self.pollvote_manager))

    def http_user_bid_prize(self, args):
        user_id = args["user_id"] if "user_id" in args else None
        prize_id = args["prize_id"] if "prize_id" in args else None

        users = self.user_manager.get(user_id, 1, show_inactive=False)
        user = users[0] if len(users) > 0 else None

        prizes = self.prize_manager.get(prize_id, 1, show_inactive=False)
        prize = prizes[0] if len(prizes) > 0 else None

        return prize.bid(user, self._fill_new_obj(args, self.prizebid_manager))

    def http_user_poll_comment(self, args):
        user_id = args["user_id"] if "user_id" in args else None
        poll_id = args["poll_id"] if "poll_id" in args else None

        users = self.user_manager.get(user_id, 1, show_inactive=False)
        user = users[0] if len(users) > 0 else None

        polls = self.poll_manager.get(poll_id, 1, show_inactive=False)
        poll = polls[0] if len(polls) > 0 else None

        return poll.add_comment(user, self._fill_new_obj(args, self.pollcomment_manager))

    def http_user_prize_comment(self, args):
        user_id = args["user_id"] if "user_id" in args else None
        poll_id = args["poll_id"] if "poll_id" in args else None

        users = self.user_manager.get(user_id, 1, show_inactive=False)
        user = users[0] if len(users) > 0 else None

        prizes = self.poll_manager.get(poll_id, 1, show_inactive=False)
        prize = prizes[0] if len(prizes) > 0 else None

        return prize.add_comment(user, self._fill_new_obj(args, self.prizecomment_manager))



if __name__ == "__main__":
    GingerAle(argv[1])
