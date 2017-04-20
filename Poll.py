from GObject import GObject, GObjectManager, F


class Poll(GObject):
    def __init__(self, logger, db, manager, question=None, choices=None, reward_tokens=None, expiration=None):
        super().__init__(logger, db, manager)
        self.question = question
        self.choices = choices
        self.reward_tokens = reward_tokens
        self.expiration = expiration

    def vote(self, user, pollvote):

        if user is None:
            return {"vote": False, "reason": F.INVALID_USER}

        if pollvote.choice not in self.choices: #to do - choice
            return {"vote": False, "reason": F.INVALID_POLL_CHOICE}

        if not any(e['user'] == user for e in self.votes):
            return {"bid": False, "reason": GC.USER_ALREADY_VOTED}

        self.votes.append({
            "timestamp": datetime.utcnow(),
            "user": user,
            "option": choice
        })

        ret = {"vote": True, "reason": ""}
        self.logger.log("Vote Poll:{} User:{} Option:{}. {}".format(
            self.id, user.id, choice, ret)
        )
        return ret


class PollManager(GObjectManager):
    @property
    def obj_class(self):
        return Poll

    @property
    def obj_collection(self):
        return "polls"
