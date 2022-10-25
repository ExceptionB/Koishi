from common import unixtime

class Session(dict):
    def __init__(self,user_id) -> None:
        self.user_id = user_id
        self.timestamp = unixtime()

    def __lt__(self,expire_time:int) -> bool:
        return (unixtime() - self.timestamp) < expire_time

    def __call__(self):
        self.timestamp = unixtime()

    def __eq__(self, __o: object) -> bool:
        return __o is Session and self.user_id == __o.user_id

    def __hash__(self) -> int:
        return self.user_id.__hash__()
    
    def __getitem__(self, __key):
        self()
        return super().__getitem__(__key)
    
    def __delitem__(self, __key) -> None:
        self()
        return super().__delitem__(__key)

    def __setitem__(self, __key, __value) -> None:
        self()
        return super().__setitem__(__key, __value)

class SessionManager(dict):
    def __init__(self,expire_time:int) -> None:
        self.expire_time = expire_time

    def __call__(self):
        for x in self:
            if not self[x] < self.expire_time:
                self.__delitem__(x)

    def __contains__(self, __o: object) -> bool:
        self()
        return super().__contains__(__o)

    def __getitem__(self, __key: int) -> Session:
        self()
        return super().__getitem__(__key)
    
    def __setitem__(self, __key: int, __value: Session) -> None:
        self()
        return super().__setitem__(__key, __value)