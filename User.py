from GObject import GObject, GObjectManager


class User(GObject):
    def __init__(self, logger, db, manager, name=None, status=None, tokens=None):
        super().__init__(logger, db, manager)
        self.name = name
        self.status = status
        self.tokens = tokens


class UserManager(GObjectManager):
    obj_class = User
    obj_collection = "users"

