import GlobalConstants as GC
from GObjects import GObject, GObjects


class Polls(GObjects):
    def __init__(self, logger, db, gifts):
        self.gifts = gifts
        super().__init__(logger, db)

        polls_db = self.db.get_polls()
        for p in polls_db:
            self[p["poll_id"]] = Poll(
                self.logger,
                self.db,
                p["poll_id"],
                p["question"],
                p["options"],
                p["token_reward"],
                gifts[p["gift_id"]]
            )

        self.logger.log("polls loaded:", str(len(polls_db)))


class Poll(GObject):
    def __init__(self, logger, db, poll_id, question, options, token_reward, gift):
        self.poll_id = poll_id
        self.question = question
        self.options = options
        self.gift = gift
        self.token_reward = token_reward
        super().__init__(logger, db)

    def vote(self, user, option):

        if not (option in self.options):
            return {"vote": False, "reason": GC.BAD_POLL_OPTION}

        return {"vote": True, "reason": ""}


