
class Index:
    def __init__(self, key, page_offset):
        self.key = key
        self.page_offset = page_offset

    def get_key(self):
        return self.key

    def get_page_offset(self):
        return self.page_offset
