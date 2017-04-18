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
    def __init__(self, request, client_address, server):
        self.get_method = {
            "bid": self.bid,
            "vote_poll": self.vote_poll,
            "polls": self.polls,
            "users": self.users,
            "gifts": self.gifts
        }
        super().__init__(request, client_address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        try:
            parsed_url = urlparse(self.path)
            parsed_query = parse_qs(parsed_url.query)

            args = json.loads(parsed_query["args"][0])
            method = parsed_url.path[1:]

            ret = json.dumps(
                self.get_method[method](args),
                sort_keys=False,
                indent=4,
                separators=(',', ': ')
            )
        except Exception as ex:
            ret = '{{"Error": "{}"}}'.format(ex)

        b = bytearray()
        b.extend(ret.encode())
        self.wfile.write(b)

    def vote_poll(self, args):
        user_id = args["user_id"],
        poll_id = args["poll_id"],
        option = args["option"],

        user = GingerAle.users[user_id]
        poll = GingerAle.polls[poll_id]

        if user is None:
            return {"vote": False, "reason": GC.INVALID_USER}

        if poll is None:
            return {"vote": False, "reason": GC.INVALID_POLL}

        return poll.vote(user, option)

    def polls(self, args):
        details = True if ("details" in args and args["details"]) else False
        top = args["top"] if "top" in args else 0
        id_filter = args["id"] if "id" in args else None
        polls = GingerAle.polls.g(id_filter, top)
        return [poll.to_dict(details) for poll in polls] if type(polls) is list else polls.to_dict(details)

    def gifts(self, args):
        top = args["top"] if "top" in args else 0
        id_filter = args["id"] if "id" in args else None
        gifts = GingerAle.polls.g(id_filter, top)
        return [gift.to_dict() for gift in gifts] if type(gifts) is list else gifts.to_dict()

    def users(self, args):
        top = args["top"] if "top" in args else 0
        id_filter = args["id"] if "id" in args else None
        users = GingerAle.users.g(id_filter, top)
        return [user.to_dict() for user in users] if type(users) is list else users.to_dict()

    def bid(self, args):
        user_id = args["user_id"],
        gift_id = args["gift_id"],
        tokens =  args["tokens"],

        user = GingerAle.users[user_id]
        gift = GingerAle.gifts[gift_id]

        if user is None:
            return {"bid": False, "reason": GC.INVALID_USER}

        if gift is None:
            return {"bid": False, "reason": GC.INVALID_GIFT}

        return gift.bid(user, tokens)


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
