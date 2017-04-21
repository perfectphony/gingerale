from Poll import PollManager
from User import UserManager
from Prize import PrizeManager
from PollComment import PollCommentManager
from PrizeComment import PrizeCommentManager
from PrizeBid import PrizeBidManager
from PollVote import PollVoteManager


class GingerAlePartial:
    def __init__(self, logger, db):
        self.logger = logger
        self.db = db
        self.user_manager = UserManager(self.logger, self.db)
        self.prize_manager = PrizeManager(self.logger, self.db)
        self.poll_manager = PollManager(self.logger, self.db)
        self.pollvote_manager = PollVoteManager(self.logger, self.db)
        self.prizebid_manager = PrizeBidManager(self.logger, self.db)
        self.pollcomment_manager = PollCommentManager(self.logger, self.db)
        self.prizecomment_manager = PrizeCommentManager(self.logger, self.db)

    def _get_objs(self, args, manager):
        show_deleted = True if ("show_deleted" in args and args["show_deleted"]) else False
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

    def http_pollcomments(self, args):
        return self._get_objs(args, self.pollcomment_manager)

    def http_pollcomment_set(self, args):
        return self._set_obj(args, self.pollcomment_manager)

    def http_pollcomments_del(self, args):
        return self._delete_objs(args, self.pollcomment_manager)

    def http_prizecomments(self, args):
        return self._get_objs(args, self.prizecomment_manager)

    def http_prizecomment_set(self, args):
        return self._set_obj(args, self.prizecomment_manager)

    def http_prizecomments_del(self, args):
        return self._delete_objs(args, self.prizecomment_manager)