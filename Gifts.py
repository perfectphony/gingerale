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
                    g["winner_user_id"]
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
                    g["winner_user_id"]
                )

        self.logger.log("gifts loaded:", str(len(gifts_db)))

    @abc.abstractmethod
    def bid(self, user, tokens):
        pass


class Gift(GObject):
    def __init__(self, logger, db, gift_id, gift_type, desc, entries, winner_user_id=-1):
        self.gift_id = gift_id
        self.gift_type = gift_type
        self.desc = desc
        self.entries = entries
        self.winner_user_id = winner_user_id
        super().__init__(logger, db)


class RaffleGift(Gift):
    def __init__(self, logger, db, gift_id, desc, entries, expiration, winner_user_id=-1):
        self.expiration = expiration
        super().__init__(logger, db, gift_id, "raffle", desc, entries, winner_user_id)

    def bid(self, user, tokens):
        if not any(e['user'] == user for e in self.entries):
            return {"bid": False, "reason": GC.USER_ALREADY_BID}

        self.entries.append({
            "timestamp": datetime.utcnow(),
            "user": user,
            "tokens": tokens
        })

        user.tokens += tokens

        return {"bid": True, "reason": ""}


class AccretionGift(Gift):
    def __init__(self, logger, db, gift_id, desc, entries, requirement, winner_user_id=-1):
        self.requirement = requirement
        super().__init__(logger, db, gift_id, "accretion", desc, entries, winner_user_id)

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

        return {"bid": True, "reason": ""}

