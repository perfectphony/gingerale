import abc


class F:
    INVALID_USER = "INACTIVE_OR_INVALID_USER"
    INVALID_POLL = "EXPIRED_OR_INVALID_POLL"
    INVALID_PRIZE = "EXPIRED_OR_INVALID_PRIZE"
    INVALID_POLL_CHOICE = "INVALID_POLL_CHOICE"
    INVALID_TOKEN_AMOUNT = "INVALID_TOKEN_AMOUNT"
    NOT_ENOUGH_TOKENS = "NOT_ENOUGH_TOKENS"
    NOT_ENOUGH_BIDS = "NOT_ENOUGH_BIDS"
    USER_ALREADY_VOTED = "USER_ALREADY_VOTED"


class GObject(metaclass=abc.ABCMeta):
    def __init__(self, logger, db, manager):
        self.id = None #auto-filled
        self.create_timestamp = None
        self.delete_timestamp = None
        self.logger = logger
        self.db = db
        self.manager = manager

    def to_dict(self, full=True):
        # full=False will prevent null fields (fields with None)
        # from being added to the dictionary

        return {
            k: v for k, v in self.__dict__.items()
            if not hasattr(v, "__dict__") and (v is not None or full)
        }

        # for k, v in self.__dict__.items():
        #     if not hasattr(v, "__dict__") and (v is not None or full):
        #         obj_dict[k] = v

        # return obj_dict

    def set(self):
        ret = self.db.set(self.manager.obj_collection, self)
        self.logger.log("Set {}:{}. {}".format(
            self.__class__.__name__, self.id, ret)
        )
        return ret


class GObjectManager(metaclass=abc.ABCMeta):

    # obj_class and obj_collection
    # must be assigned by the inheriting class

    # used to create new instances of the object
    @property
    @abc.abstractmethod
    def obj_class(self):
        return None

    # used to insert record into database collection/table name
    @property
    @abc.abstractmethod
    def obj_collection(self):
        return None

    def __init__(self, logger, db):
        self.logger = logger
        self.db = db

    def delete(self, id_list):
        ret = self.db.delete(self.obj_collection, id_list)
        self.logger.log("Delete {}:{}. {}".format(
            self.obj_class.__class__.__name__, id_list, ret)
        )
        return ret

    def get(self, id_list, limit=0, show_inactive=True, show_deleted=False):
        return self.db.get(self.obj_collection, self.obj_class, self, id_list, limit, show_inactive, show_deleted)
