from threading import RLock

from database import MongoDB

INSERTION_LOCK = RLock()


class USERS(MongoDB):
    """
    To store user id
    """

    db_name = "user"

    def __init__(self) -> None:
        super().__init__(self.db_name)

    def insert_user(self, _id, u_type):
        curr = self.find_one({"peer": _id})
        if not curr:
            self.insert_one({"peer": _id, "type": u_type})
        return

    def get_all_users(self, u_type="all"):
        if u_type == "all":
            curr = self.find_all({})
            if curr:
                peer = [int(i['peer']) for i in list(curr)]
            else:
                peer = []
        elif u_type == "chat":
            curr = self.find_all({"type": "chat"})
            if curr:
                peer = [int(i['peer']) for i in list(curr)]
            else:
                peer = []
        else:
            curr = self.find_all({"type": "user"})
            if curr:
                peer = [int(i['peer']) for i in list(curr)]
            else:
                peer = []
        return peer
