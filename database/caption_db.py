from threading import RLock

from database import MongoDB

INSERTION_LOCK = RLock()


class CAPTION(MongoDB):
    """
    is caption content
    """

    db_name = "caption"

    def __init__(self) -> None:
        super().__init__(self.db_name)

    def load_caption(self, caption=None):
        curr = self.find_all({})
        if not curr:
            self.insert_one({"caption": caption})
            return False
        return True

    def get_caption(self):
        curr = self.find_all({})
        if curr:
            return list(curr)[0]['caption']
        return None

    def update_caption(self, caption):
        old_cap = self.get_caption()
        curr = self.find_one({"caption": old_cap})
        if curr:
            with INSERTION_LOCK:
                self.update({"_id": curr['_id']}, {"caption": caption})
        return

    def remove_caption(self):
        curr = self.get_caption()
        if curr:
            self.delete_one({"caption": curr})
        return
