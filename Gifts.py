from datetime import datetime
import abc

import GlobalConstants as GC
from GObjects import GObject, GObjects


class Gift(GObject):
    def __init__(self, logger, db, gift_id, desc, entries, requirement, winner=None):
        self.desc = desc
        self.entries = entries
        self.requirement = requirement
        self.winner = winner
        super().__init__(logger, db, gift_id)

    def to_dict(self):
        ret = super().to_dict()
        ret.update({
            "desc": self.desc,
            "entries": [{
                "timestamp": e["timestamp"].isoformat('T'),
                "user": e["user"].user_id,
                "tokens": e["tokens"]
            } for e in self.entries],
            "requirement": self.requirement,
            "winner_user_id": self.winner.user_id
        })
        return ret

    def bid(self, user, tokens):

        if user.tokens < tokens:
            return {"bid": False, "reason": GC.NOT_ENOUGH_TOKENS}

        entry = self.entries.append({
            "timestamp": datetime.utcnow(),
            "user": user,
            "tokens": tokens
        })

        total_bid_tokens = sum(e['tokens'] for e in self.entries)

        if total_bid_tokens < self.requirement:
            return {"bid": False, "reason": GC.NOT_ENOUGH_BIDS}

        #return token over usage to user
        token_overflow = total_bid_tokens - self.requirement
        user.give_tokens(token_overflow)
        entry["tokens"] -= token_overflow
        self.winner = user

        return {"bid": True, "reason": ""}


class Gifts(GObjects):
    underlying_type = Gift

    def __init__(self, logger, db, users):
        self.users = users
        super().__init__(logger, db)

        gifts_db = self.db.get_gifts()

        for g in gifts_db:
            self[g["id"]] = Gift(
                self.logger,
                self.db,
                g["id"],
                g["desc"],
                [{
                    "timestamp": e["timestamp"],
                    "user": users.get(e["user_id"]),
                    "tokens": e["tokens"]
                } for e in g["entries"]],
                g["requirement"],
                None if g["winner_user_id"] < 0 else users.get(g["winner_user_id"])
            )

        self.logger.log("gifts loaded:", str(len(gifts_db)))

    @abc.abstractmethod
    def bid(self, user, tokens):
        pass


