import abc


class GObjectManager(metaclass=abc.ABCMeta):
    def __init__(self, logger, db):
        self.logger = logger
        self.db = db
        self.manager = None #filled by inherited class object

    def delete(self, id_list):
        return self.db.delete(self.obj_collection, id_list)

    def get(self, id_list, limit=0, show_deleted=False):
        return self.db.get(self.obj_collection, self.obj_class, self, id_list, limit, show_deleted)


class GObject(metaclass=abc.ABCMeta):
    #filled by inherited classes
    obj_class = None
    obj_collection = None

    def __init__(self, logger, db, manager):
        self.id = None #auto-filled
        self.create_timestamp = None
        self.delete_timestamp = None
        self.logger = logger
        self.db = db
        self.manager = manager

    def to_dict(self, full=True):
        obj_dict = {}

        for k, v in self.__dict__.items():
            if not hasattr(v, "__dict__") \
            and (v is not None or full):
                obj_dict[k] = v

        return obj_dict

    def set(self):
        return self.db.set(self.manager.obj_collection, self)