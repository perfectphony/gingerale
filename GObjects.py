import abc


class GObject(metaclass=abc.ABCMeta):
    def __init__(self, logger, db, manager, object_id):
        self.logger = logger
        self.db = db
        self.manager = manager
        self.id = object_id

    def to_dict(self):
        obj_dict = {}

        for k, v in self.__dict__.items():
            if not hasattr(v, "__dict__"):
                obj_dict[k] = v

        return obj_dict


class GObjectManager(metaclass=abc.ABCMeta):
    underlying_type = GObject

    def __init__(self, logger, db):
        self.logger = logger
        self.db = db
