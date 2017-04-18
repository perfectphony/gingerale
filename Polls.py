from datetime import datetime
import GlobalConstants as GC
from GObjects import GObject, GObjects


class Poll(GObject):
    def __init__(self, logger, db, poll_id, question, options, votes, reward_tokens, gift):
        self.question = question
        self.options = options
        self.votes = votes
        self.gift = gift
        self.reward_tokens = reward_tokens
        super().__init__(logger, db, poll_id)

    def to_dict(self, details=True):
        ret = super().to_dict()
        ret.update({
            "question": self.question,
            "options": [
                {
                    "option": o["option"],
                    "text": o["text"],
                    "count": sum(1 for v in self.votes if o["option"] == v["option"])
                } for o in self.options
            ],
            "votes": [{
                "timestamp": v["timestamp"].isoformat('T'),
                "user": v["user"].id,
                "option": v["option"]
            } for v in self.votes] if details else len(self.votes),
            "gift": self.gift.id,
            "reward_tokens": self.reward_tokens
        })
        return ret

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


class Polls(GObjects):
    underlying_type = Poll

    def __init__(self, logger, db, gifts, users):
        self.gifts = gifts
        self.users = users
        super().__init__(logger, db)

        polls_db = self.db.get_polls()
        for p in polls_db:
            self[p["id"]] = Poll(
                self.logger,
                self.db,
                p["id"],
                p["question"],
                p["options"],
                [{
                    "timestamp": v["timestamp"],
                    "user": users.get(v["user_id"]),
                    "option": v["option"]
                } for v in p["votes"]],
                p["reward_tokens"],
                gifts.get(p["gift_id"])
            )

        self.logger.log("polls loaded:", str(len(polls_db)))

