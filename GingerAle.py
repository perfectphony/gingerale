# example usage: Python GingerAle port=6176 max_threads=10
# port: port number gingerale will listen on for incoming connections
# max_threads: number of simultaneous threads to use (thread pool)

from sys import argv
from concurrent.futures import ThreadPoolExecutor

# modular classes
from DatabaseMongoDB import Database
from LoggerNone import Logger
from HttpRequestTornado import HttpRequest

# partial class for GingerAle
from GingerAlePartial import GingerAlePartial


class GingerAle(GingerAlePartial):
    def __init__(self, port, max_threads):
        logger = Logger()
        db = Database(logger)
        super().__init__(logger, db)

        thread_pool = ThreadPoolExecutor(max_workers=max_threads)

        logger.log("GingerAle started.")
        HttpRequest(self, port, thread_pool)

        self.logger.log("GingerAle exiting...")
        db.close()
        logger.close()

    def http_test(self, args):
        t = {}
        for i in range(0, 10000):
            t[i] = self._get_objs({"id": [500, 501]}, self.poll_manager)
        return t

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

    # parse parameters to dictionary, example argument: port=6176
    cmd_line_args = {arg.split("=")[0]: arg.split("=")[1] for arg in argv[1:]}

    GingerAle(
        port=cmd_line_args["port"] if "port" in cmd_line_args else 6176,
        max_threads=cmd_line_args["max_threads"] if "max_threads" in cmd_line_args else 10
    )
