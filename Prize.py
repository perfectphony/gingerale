from GObject import GObject, GObjectManager, F


class Prize(GObject):
    def __init__(self, logger, db, manager, desc=None, entries=None, requirement=None, winner_user_id=None):
        super().__init__(logger, db, manager)
        self.desc = desc
        self.entries = entries
        self.requirement = requirement
        self.winner_user_id = winner_user_id

    def bid(self, user, prizebid):

        #to do - make concurrent safe
        if user is None:
            return {"bid": False, "reason": F.INVALID_PRIZE}

        if user.tokens < prizebid.tokens:
            return {"bid": False, "reason": F.NOT_ENOUGH_TOKENS}

        total_bid_tokens = 0 + prizebid.tokens #to do

        if total_bid_tokens < self.requirement:
            return {"bid": False, "reason": F.NOT_ENOUGH_BIDS}

        #return token over usage to user
        token_overflow = total_bid_tokens - self.requirement
        user.give_tokens(token_overflow)
        entry["tokens"] -= token_overflow
        self.winner_user = user

        ret = {"bid": True, "reason": ""}
        self.logger.log("Bid Prize:{} User:{} Tokens:{}. {}".format(
            self.id, user.id, prizebid.tokens, ret)
        )
        return ret


class PrizeManager(GObjectManager):
    @property
    def obj_class(self):
        return Prize

    @property
    def obj_collection(self):
        return "prizes"
