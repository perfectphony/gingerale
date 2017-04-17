import abc


class GObjects(dict, metaclass=abc.ABCMeta):
    def __init__(self, logger, db):
        self.logger = logger
        self.db = db
        super().__init__()

    def g(self, object_id):

        try:
            object_id = int(object_id)
        except:
            return None

        return self[object_id]


class GObject(metaclass=abc.ABCMeta):
    def __init__(self, logger, db):
        self.logger = logger
        self.db = db

    @abc.abstractmethod
    def to_dict(self):
        pass
