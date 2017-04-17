import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import GlobalConstants as GC
from DatabaseTest import Database
from LoggerNone import Logger

from Polls import Polls
from Users import Users
from Gifts import Gifts


class HttpRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        parsed_url = urlparse(self.path)
        parsed_query = parse_qs(parsed_url.query)
        method = parsed_url.path[1:]

        ret = self.switch(method, parsed_query)
        b = bytearray()
        b.extend(ret.encode())
        self.wfile.write(b)

    def switch(self, method, args):

        ret = {}
        if method == "check_user_authorization":
            ret = self.check_user_authorization(args["user_id"][0])
        elif method == "bid":
            ret = self.bid_gift(
                args["user_id"][0],
                args["gift_id"][0],
                args["tokens"][0],
            )
        elif method == "vote_poll":
            ret = self.vote_poll(
                args["user_id"][0],
                args["poll_id"][0],
                args["option"][0],
            )
        elif method == "view_poll":
            ret = self.view_poll(args["poll_id"][0])

        return json.dumps(
            ret,
            sort_keys=False,
            indent=4,
            separators=(',', ': ')
        )

    def vote_poll(self, user_id, poll_id, option):
        user = GingerAle.users.g(user_id)
        poll = GingerAle.polls.g(poll_id)

        if user is None:
            return {"vote": False, "reason": GC.INVALID_USER}

        if poll is None:
            return {"vote": False, "reason": GC.INVALID_POLL}

        bid_raffle = self.bid_gift(user_id, poll.gift.gift_id, poll.token_reward)

        if not bid_raffle["bid"]:
            return {"vote": False, "reason": bid_raffle["reason"]}

        return poll.vote(user, option)

    def view_poll(self, poll_id):
        poll = GingerAle.polls.g(poll_id)

        if poll is None:
            return {}

        return poll.to_dict()

    def bid_gift(self, user_id, gift_id, tokens):
        user = GingerAle.users.g(user_id)
        gift = GingerAle.gifts.g(gift_id)

        if user is None:
            return {"bid": False, "reason": GC.INVALID_USER}

        if gift is None:
            return {"bid": False, "reason": GC.INVALID_GIFT}

        return gift.bid(user, tokens)

    def check_user_authorization(self, user_id):
        user = GingerAle.users.g(user_id)

        if user is None:
            return {"authorized": False, "reason": GC.INVALID_USER}

        return {"authorized": True, "reason": ""}


class GingerAle:
    logger = Logger()
    db = Database()

    users = Users(logger, db)
    gifts = Gifts(logger, db, users)
    polls = Polls(logger, db, gifts, users)

    def __init__(self, port):
        self.logger.log("GingerAle starting...")

        httpd = HTTPServer(('', port), HttpRequestHandler)
        try:
            self.logger.log("GingerAle running on port", port)
            httpd.serve_forever()

        except KeyboardInterrupt:
            self.logger.log("GingerAle shutting down...")
            httpd.server_close()


if __name__ == "__main__":
    GingerAle(port=6176)
