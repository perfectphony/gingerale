from datetime import datetime
import abc

import GlobalConstants as GC
from GObjects import GObject, GObjects


class Gifts(GObjects):
    def __init__(self, logger, db, users):
        self.users = users
        super().__init__(logger, db)

        gifts_db = self.db.get_gifts()

        for g in gifts_db:
            if g["gift_type"] == "raffle":
                self[g["gift_id"]] = RaffleGift(
                    self.logger,
                    self.db,
                    g["gift_id"],
                    g["desc"],
                    [{
                        "timestamp": e["timestamp"],
                        "user": users[e["user_id"]],
                        "tokens": e["tokens"]
                    } for e in g["entries"]],
                    g["expiration"],
                    None if g["winner_user_id"] < 0 else users[g["winner_user_id"]]
                )
            elif g["gift_type"] == "accretion":
                self[g["gift_id"]] = AccretionGift(
                    self.logger,
                    self.db,
                    g["gift_id"],
                    g["desc"],
                    [{
                        "timestamp": e["timestamp"],
                        "user": users[e["user_id"]],
                        "tokens": e["tokens"]
                    } for e in g["entries"]],
                    g["requirement"],
                    None if g["winner_user_id"] < 0 else users[g["winner_user_id"]]
                )

        self.logger.log("gifts loaded:", str(len(gifts_db)))

    @abc.abstractmethod
    def bid(self, user, tokens):
        pass


class Gift(GObject):
    def __init__(self, logger, db, gift_id, gift_type, desc, entries, winner=None):
        self.gift_id = gift_id
        self.gift_type = gift_type
        self.desc = desc
        self.entries = entries
        self.winner = winner
        super().__init__(logger, db)

    def to_dict(self):
        return {
            "gift_id": self.gift_id,
            "gift_type": self.gift_type,
            "desc": self.desc,
            "entries": [{
                "timestamp": e["timestamp"].isoformat('T'),
                "user": e["user"].user_id,
                "tokens": e["tokens"]
            } for e in self.entries],
            "winner_user_id": self.winner.user_id
        }


class RaffleGift(Gift):
    def __init__(self, logger, db, gift_id, desc, entries, expiration, winner=None):
        self.expiration = expiration
        super().__init__(logger, db, gift_id, "raffle", desc, entries, winner)

    def bid(self, user, tokens):
        if not any(e['user'] == user for e in self.entries):
            return {"bid": False, "reason": GC.USER_ALREADY_BID}

        self.entries.append({
            "timestamp": datetime.utcnow().isoformat('T'),
            "user": user,
            "tokens": tokens
        })

        user.tokens += tokens

        return {"bid": True, "reason": ""}

    def to_dict(self):
        return super().to_dict().update({
            "expiration": self.expiration
        })


class AccretionGift(Gift):
    def __init__(self, logger, db, gift_id, desc, entries, requirement, winner=None):
        self.requirement = requirement
        super().__init__(logger, db, gift_id, "accretion", desc, entries, winner)

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

    def to_dict(self):
        return super().to_dict().update({
            "requirement": self.requirement
        })
