import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import GlobalConstants as GC
from DatabaseMongoDB import Database
from LoggerNone import Logger

from Poll import PollManager
from User import UserManager
from Gift import GiftManager


class HttpRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.get_method = {
            "gift_bid": self.gift_bid,
            "poll_vote": self.poll_vote,
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
                separators=(',', ': '),
                default=lambda obj: obj.isoformat('T') if type(obj) is datetime else None,
                skipkeys=True
            )
        except Exception as ex:
            ret = '{{"Error": "{}"}}'.format(ex)

        b = bytearray()
        b.extend(ret.encode())
        self.wfile.write(b)

    def polls(self, args):
        show_details = True if ("show_details" in args and args["show_details"]) else False
        limit = args["limit"] if "limit" in args else 0
        id_filter = args["id"] if "id" in args else None

        polls = GingerAle.poll_manager.get(id_filter, limit)
        return [poll.to_dict() for poll in polls]

    def gifts(self, args):
        show_details = True if ("show_details" in args and args["show_details"]) else False
        limit = args["limit"] if "limit" in args else 0
        id_filter = args["id"] if "id" in args else None

        gifts = GingerAle.poll_manager.get(id_filter, limit)
        return [gift.to_dict() for gift in gifts]

    def users(self, args):
        show_details = True if ("show_details" in args and args["show_details"]) else False
        limit = args["limit"] if "limit" in args else 0
        id_filter = args["id"] if "id" in args else None

        users = GingerAle.poll_manager.get(id_filter, limit)
        return [user.to_dict() for user in users]

    def poll_vote(self, args):
        user_id = args["user_id"],
        poll_id = args["poll_id"],
        option = args["option"],

        user = GingerAle.user_manager.get(user_id)
        poll = GingerAle.poll_manager.get(poll_id)

        if user is None:
            return {"vote": False, "reason": GC.INVALID_USER}

        if poll is None:
            return {"vote": False, "reason": GC.INVALID_POLL}

        return poll.vote(user, option)

    def gift_bid(self, args):
        user_id = args["user_id"],
        gift_id = args["gift_id"],
        tokens = args["tokens"],

        user = GingerAle.user_manager.get(user_id)
        gift = GingerAle.gift_manager.get(gift_id)

        if user is None:
            return {"bid": False, "reason": GC.INVALID_USER}

        if gift is None:
            return {"bid": False, "reason": GC.INVALID_GIFT}

        return gift.bid(user, tokens)


class GingerAle:
    logger = Logger()
    db = Database(logger)

    user_manager = UserManager(logger, db)
    gift_manager = GiftManager(logger, db, user_manager)
    poll_manager = PollManager(logger, db, gift_manager, user_manager)

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
