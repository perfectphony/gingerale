from datetime import datetime
import abc

import GlobalConstants as GC
from GObjects import GObject, GObjectManager


class GiftManager(GObjectManager):
    def __init__(self, logger, db, user_manager):
        self.user_manager = user_manager
        super().__init__(logger, db)

    def get(self, id_filter, limit=0):
        return self.db.get("polls", Gift, self, id_filter, limit)


class Gift(GObject):
    def __init__(self, logger, db, manager, gift_id, desc=None, entries=None, requirement=None, winner_user=None):
        self.desc = desc
        self.entries = entries
        self.requirement = requirement
        self.winner_user = winner_user
        super().__init__(logger, db, manager, gift_id)

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
        self.winner_user = user

        return {"bid": True, "reason": ""}


