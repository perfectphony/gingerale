from GObject import GObjectManager
from Comment import Comment


class PrizeComment(Comment):
    def __init__(self, logger, db, manager, text=None, user_id=None, prize_id=None):
        super().__init__(logger, db, manager, text, user_id)
        self.prize_id = prize_id


class PrizeCommentManager(GObjectManager):
    @property
    def obj_class(self):
        return PrizeComment

    @property
    def obj_collection(self):
        return "prizecomments"
