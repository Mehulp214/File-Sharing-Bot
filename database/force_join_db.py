from threading import RLock

from database import MongoDB

INSERTION_LOCK = RLock()


class FSUBS(MongoDB):
    """
    class to store fsub channels in database
    request, direct
    """

    db_name = "fsub_channel"

    def __init__(self) -> None:
        super().__init__(self.db_name)

    def inser_fsub(self, channel_id):
        """
        channeld_id: Int type id of the channel
        """
        curr = self.find_one({'c_id': channel_id})
        if not curr:
            self.insert_one({"c_id": channel_id})
            return False
        else:
            return True

    def remove_fsub(self, channel_id):
        curr = self.find_one({'c_id': channel_id})
        if curr:
            self.delete_one({'c_id': channel_id})
        return

    def remove_all(self):
        curr = self.find_all({})
        if curr:
            for i in list(curr):
                self.delete_one({'c_id': i['c_id']})
        return

    def get_fsubs(self):
        """
        type: Type you want to fetch default to all.

        """
        curr = self.find_all({})
        if curr:
            curr = [int(i['c_id']) for i in list(curr)]
        else:
            curr = []
        return curr
