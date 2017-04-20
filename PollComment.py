from GObject import GObjectManager
from Comment import Comment


class PollComment(Comment):
    def __init__(self, logger, db, manager, text=None, user_id=None, poll_id=None):
        super().__init__(logger, db, manager, text, user_id)
        self.poll_id = poll_id


class PollCommentManager(GObjectManager):
    @property
    def obj_class(self):
        return PollComment

    @property
    def obj_collection(self):
        return "pollcomments"
