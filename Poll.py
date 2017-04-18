from datetime import datetime
import GlobalConstants as GC
from GObjects import GObject, GObjectManager


class PollManager(GObjectManager):
    def __init__(self, logger, db, gift_manager, users_manager):
        self.gift_manager = gift_manager
        self.users_manager = users_manager
        super().__init__(logger, db)

    def get(self, id_filter, limit=0):
        return self.db.get("polls", Poll, self, id_filter, limit)

    def set(self, poll):
        if not isinstance(poll, self.underlying_type):
            raise Exception("{} - attempted to insert invalid object type".format(self.__class__.__name__))

        #to do - update db


class Poll(GObject):
    def __init__(self, logger, db, manager, poll_id, question=None, options=None, votes=None, reward_tokens=None, gift_id=None):
        self.question = question
        self.options = options
        self.votes = votes
        self.reward_tokens = reward_tokens
        self.gift_id = gift_id
        super().__init__(logger, db, manager, poll_id)

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

