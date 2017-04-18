from GObjects import GObject, GObjects


class User(GObject):
    def __init__(self, logger, db, user_id, name, status, tokens):
        self.logger = logger
        self.db = db
        self.name = name
        self.status = status
        self.tokens = tokens
        super().__init__(logger, db, user_id)

    def to_dict(self):
        ret = super().to_dict()
        ret.update({
            "name": self.name,
            "status:": self.status,
            "tokens": self.tokens
        })
        return ret


class Users(GObjects):
    underlying_type = User

    def __init__(self, logger, db):
        super().__init__(logger, db)

        users_db = self.db.get_users()

        for u in users_db:
            self[u["id"]] = User(self.logger, self.db, u["id"], u["name"], u["status"], u["tokens"])

        self.logger.log("users loaded:", str(len(users_db)))

    def __getitem__(self, item):
        ret = super().__getitem__(item)
        return ret if ret.status == "active" else None
