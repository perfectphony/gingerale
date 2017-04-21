import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from tornado import web, ioloop

from GingerAleInit import GingerAleInit


class WebHandler(web.RequestHandler):
    def initialize(self, GA):
        self.GA = GA

    #@gen.coroutine
    @web.asynchronous
    def get(self):
        self.GA.thread_pool.submit(self.respond)

    def respond(self):
        if self.request.uri == "/favicon.ico":
            return

        self.GA.logger.log(self.request.uri)

        parsed_url = urlparse(self.request.uri)
        parsed_query = parse_qs(parsed_url.query)

        args = json.loads(parsed_query["args"][0]) if "args" in parsed_query else {}
        method = "http_" + parsed_url.path[1:]

        ret = json.dumps(
            self.GA.__getattribute__(method)(args),
            sort_keys=False,
            indent=4,
            separators=(',', ': '),
            default=lambda obj: obj.isoformat('T') if type(obj) is datetime else None,
            skipkeys=True
        )

        self.set_header('Content-Type', 'application/json')
        self.write(ret)
        self.finish()


class GingerAle(GingerAleInit):
    def __init__(self, port, max_threads):
        super().__init__()
        self.thread_pool = ThreadPoolExecutor(max_workers=max_threads)

        try:
            server_app = web.Application([(r"/.*", WebHandler, {"GA": self})])
            server_app.listen(port)
            self.logger.log("GingerAle running")
            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            ioloop.IOLoop.instance().stop()
            self.logger.log("GingerAle exiting...")
            self.db.close()
            self.logger.close()

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
    GingerAle(6176, 10)
