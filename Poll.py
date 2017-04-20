from GObject import GObjectManager, F
from Comment import CommentContainer


class Poll(CommentContainer):
    def __init__(self, logger, db, manager, question=None, choices=None, reward_tokens=None, expiration=None):
        super().__init__(logger, db, manager)
        self.question = question
        self.choices = choices  # list, ex: {"value": 0, "text": "Yes"}
        self.reward_tokens = reward_tokens
        self.expiration = expiration

    def vote(self, user, pollvote):

        if user is None:
            return {"inserted": 0, "reason": F.INVALID_USER}

        if not any(c["value"] == pollvote.choice for c in self.choices):
            return {"inserted": 0, "reason": F.INVALID_POLL_CHOICE}

        if self.db.get_vote_by_poll_and_user(user.id, self.id) is not None:
            return {"inserted": 0, "reason": F.USER_ALREADY_VOTED}

        self.logger.log("Vote Poll:{} User:{} Option:{}".format(
            self.id, user.id, pollvote.choice)
        )
        return pollvote.set()


class PollManager(GObjectManager):
    @property
    def obj_class(self):
        return Poll

    @property
    def obj_collection(self):
        return "polls"
