from datetime import datetime

from GObject import GObject, GObjectManager


class PollVote(GObject):
    def __init__(self, logger, db, manager, poll_id=None, user_id=None, choice=None):
        super().__init__(logger, db, manager)
        self.poll_id = poll_id
        self.user_id = user_id
        self.choice = choice


class PollVoteManager(GObjectManager):
    @property
    def obj_class(self):
        return PollVote

    @property
    def obj_collection(self):
        return "pollvotes"
