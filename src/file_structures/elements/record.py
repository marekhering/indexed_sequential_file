

class Record:
    def __init__(self, key, value, next_record_pointer):
        self.key = key
        self.value = value
        self.next_record_pointer = next_record_pointer

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value
    
    def get_next_record_pointer(self):
        return self.next_record_pointer
