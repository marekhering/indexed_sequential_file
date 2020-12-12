
class Index:
    def __init__(self, key, page_number):
        self.key = key
        self.page_number = int(page_number)

    def get_key(self):
        return self.key

    def get_page_number(self):
        return self.page_number
