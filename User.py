from GObjects import GObject, GObjectManager


class UserManager(GObjectManager):
    def get(self, id_filter, limit=0):
        return self.db.get("polls", User, self, id_filter, limit)

class User(GObject):
    def __init__(self, logger, db, manager, user_id, name=None, status=None, tokens=None):
        self.name = name
        self.status = status
        self.tokens = tokens
        super().__init__(logger, db, manager, user_id)
