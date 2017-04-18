import abc


class GObject(metaclass=abc.ABCMeta):
    def __init__(self, logger, db, object_id):
        self.logger = logger
        self.db = db
        self.id = object_id

    def to_dict(self):
        return {
            "id": self.id,
            "object_type": self.__class__.__name__
        }


class GObjects(dict, metaclass=abc.ABCMeta):
    underlying_type = GObject

    def __init__(self, logger, db):

        self.logger = logger
        self.db = db
        super().__init__()

    def g(self, id_filter=None, top=0):
        id_filter = int(id_filter) if type(id_filter) is str else id_filter

        if type(id_filter) is int:
            return super()[id_filter]

        if id_filter is None:
            filtered_list = [v for k, v in self.items()]
        else:
            filtered_list = [v for k, v in self.items() if k in id_filter]

        filtered_list.sort(key=lambda obj: obj.id)

        return filtered_list if top == 0 else filtered_list[-top:]

    def __setitem__(self, key, value):
        if not isinstance(value, self.underlying_type):
            raise Exception("{} - attempted to insert invalid object type".format(self.__class__.__name__))

        super().__setitem__(key, value)

