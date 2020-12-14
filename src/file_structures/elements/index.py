from src.setup import PAGE_NUMBER_SIZE


class Index:
    def __init__(self, key, page_number):
        self.key = key
        self.page_number = int(page_number)

    def get_key(self):
        return self.key

    def get_page_number(self):
        return self.page_number

    def to_string(self):
        return self.key + ' ' + '0' * (PAGE_NUMBER_SIZE - len(str(self.page_number))) + str(self.page_number) + '\n'
