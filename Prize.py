from GObject import GObjectManager, F
from Comment import CommentContainer


class Prize(CommentContainer):
    def __init__(self, logger, db, manager, desc=None, entries=None, current_bid_count=None, required_bids=None):
        super().__init__(logger, db, manager)
        self.desc = desc
        self.entries = entries
        self.current_bid_count = current_bid_count
        self.required_bids = required_bids

    def bid(self, user, prizebid, tokens):

        if user is None:
            return {"win": False, "reason": F.INVALID_PRIZE}

        if user.tokens < prizebid.tokens:
            return {"win": False, "reason": F.NOT_ENOUGH_TOKENS}

        ret = self.db.bid_prize(self.id, user.id, tokens)

        if ret is None:
            return {"win": False, "reason": F.NOT_ENOUGH_BIDS}

        if ret > 0: #return overpaid tokens to user
            prizebid.tokens -= ret
            user.tokens -= prizebid.tokens

        #save to db
        prizebid.set()
        user.set()

        self.logger.log("WIN Bid Prize:{} User:{} Tokens:{}".format(
            self.id, user.id, prizebid.tokens)
        )
        return {"win": True}


class PrizeManager(GObjectManager):
    @property
    def obj_class(self):
        return Prize

    @property
    def obj_collection(self):
        return "prizes"
