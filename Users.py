from GObjects import GObject, GObjects


class Users(GObjects):
    def __init__(self, logger, db):
        super().__init__(logger, db)

        users_db = self.db.get_users()

        for u in users_db:
            self[u["user_id"]] = User(self.logger, self.db, u["user_id"], u["name"], u["status"], u["tokens"])

        self.logger.log("users loaded:", str(len(users_db)))

    def g(self, user_id):
        user = super().g(user_id)
        if user is None or user.status != "active":
            return None

        return user


class User(GObject):
    def __init__(self, logger, db, user_id, name, status, tokens):
        self.logger = logger
        self.db = db
        self.user_id = user_id
        self.name = name
        self.status = status
        self.tokens = tokens
        super().__init__(logger, db)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "status:": self.status,
            "tokens": self.tokens
        }
