from GObject import GObject, F


class Comment(GObject): #comment object
    def __init__(self, logger, db, manager, text=None, user_id=None):
        super().__init__(logger, db, manager)
        self.text = text
        self.user_id = user_id


class CommentContainer(GObject): #objects that contains comments
    def add_comment(self, user, comment):

        if user is None:
            return {"inserted": "0", "reason": F.INVALID_USER}

        comment.id = None
        return self.set()
