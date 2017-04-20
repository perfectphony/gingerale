from GObject import GObject, GObjectManager


class Comment(GObject):
    def __init__(self, logger, db, manager, text=None, parent_collection=None, parent_id=None, user_id=None):
        super().__init__(logger, db, manager)
        self.text = text
        self.user_id = user_id
        self.parent_collection = parent_collection
        self.parent_id = parent_id

    def user(self):
        return self.manager.user_manager.get(self.user_id, 1)[0]


class CommentManager(GObjectManager):
    @property
    def obj_class(self):
        return Comment

    @property
    def obj_collection(self):
        return "comments"
