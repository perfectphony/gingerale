from datetime import datetime
import GlobalConstants as GC
from GObject import GObject, GObjectManager


class Poll(GObject):
    def __init__(self, logger, db, manager, question=None, options=None, votes=None, reward_tokens=None, prize_id=None):
        super().__init__(logger, db, manager)
        self.question = question
        self.options = options
        self.votes = votes
        self.reward_tokens = reward_tokens
        self.prize_id = prize_id

    def prize(self):
        return self.manager.prize_manager.get(self.prize_id, 1)[0]

    def vote(self, user, option):

        if not (option in self.options):
            return {"vote": False, "reason": GC.BAD_POLL_OPTION}

        if not any(e['user'] == user for e in self.votes):
            return {"bid": False, "reason": GC.USER_ALREADY_VOTED}

        self.votes.append({
            "timestamp": datetime.utcnow(),
            "user": user,
            "option": option
        })

        ret = {"vote": True, "reason": ""}
        self.logger.log("Vote Poll:{} User:{} Option:{}. {}".format(
            self.id, user.id, option, ret)
        )
        return ret


class PollManager(GObjectManager):
    @property
    def obj_class(self):
        return Poll

    @property
    def obj_collection(self):
        return "polls"

    def __init__(self, logger, db, prize_anager, users_manager):
        self.prize_anager = prize_anager
        self.users_manager = users_manager
        super().__init__(logger, db)
