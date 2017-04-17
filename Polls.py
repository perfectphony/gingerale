from datetime import datetime
import GlobalConstants as GC
from GObjects import GObject, GObjects


class Polls(GObjects):
    def __init__(self, logger, db, gifts, users):
        self.gifts = gifts
        self.users = users
        super().__init__(logger, db)

        polls_db = self.db.get_polls()
        for p in polls_db:
            self[p["poll_id"]] = Poll(
                self.logger,
                self.db,
                p["poll_id"],
                p["question"],
                p["options"],
                [{
                    "timestamp": v["timestamp"],
                    "user": users[v["user_id"]],
                    "option": v["option"]
                } for v in p["votes"]],
                p["reward_tokens"],
                gifts[p["gift_id"]]
            )

        self.logger.log("polls loaded:", str(len(polls_db)))


class Poll(GObject):
    def __init__(self, logger, db, poll_id, question, options, votes, reward_tokens, gift):
        self.poll_id = poll_id
        self.question = question
        self.options = options
        self.votes = votes
        self.gift = gift
        self.reward_tokens = reward_tokens
        super().__init__(logger, db)

    def to_dict(self):
        return {
            "poll_id": self.poll_id,
            "question": self.question,
            "options": self.options,
            "votes":  [{
                "timestamp": v["timestamp"].isoformat('T'),
                "user": v["user"].user_id,
                "option": v["option"]
            } for v in self.votes],
            "gift": self.gift.gift_id,
            "reward_tokens": self.reward_tokens
        }

    def vote(self, user, option):

        if not (option in self.options):
            return {"vote": False, "reason": GC.BAD_POLL_OPTION}

        if not any(e['user'] == user for e in self.votes):
            return {"bid": False, "reason": GC.USER_ALREADY_VOTED}

        self.votes.append({
            "timestamp": datetime.utcnow(),
            "user": user
        })

        return {"vote": True, "reason": ""}


