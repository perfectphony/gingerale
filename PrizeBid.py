from datetime import datetime

from GObject import GObject, GObjectManager


class PrizeBid(GObject):
    def __init__(self, logger, db, manager, prize_id=None, user_id=None, tokens=None):
        super().__init__(logger, db, manager)
        self.prize_id = prize_id
        self.user_id = user_id
        self.tokens = tokens


class PrizeBidManager(GObjectManager):
    @property
    def obj_class(self):
        return PrizeBid

    @property
    def obj_collection(self):
        return "prizebids"
