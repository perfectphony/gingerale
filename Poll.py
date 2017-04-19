from datetime import datetime
import GlobalConstants as GC
from GObject import GObject, GObjectManager


class Poll(GObject):
    def __init__(self, logger, db, manager, question=None, options=None, votes=None, reward_tokens=None, gift_id=None):
        super().__init__(logger, db, manager)
        self.question = question
        self.options = options
        self.votes = votes
        self.reward_tokens = reward_tokens
        self.gift_id = gift_id

    def gift(self):
        return self.manager.gift_manager.get(self.gift_id, 1)[0]

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

        return {"vote": True, "reason": ""}


class PollManager(GObjectManager):
    obj_class = Poll
    obj_collection = "polls"

    def __init__(self, logger, db, gift_manager, users_manager):
        self.gift_manager = gift_manager
        self.users_manager = users_manager
        super().__init__(logger, db)
