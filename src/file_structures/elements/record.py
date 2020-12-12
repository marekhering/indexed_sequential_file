from src.setup import *


class Record:
    def __init__(self, key, value, next_record_pointer=None, line_number=None):
        self.key = key
        self.value = value
        self.next_record_pointer = next_record_pointer
        self.line_number = line_number

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value
    
    def get_next_record_pointer(self):
        return self.next_record_pointer

    def set_next_record_pointer(self, next_record_pointer):
        self.next_record_pointer = next_record_pointer

    def to_string(self):
        return self.key + ' ' + self.get_value_as_string() + ' ' + self.get_next_record_pointer_as_string() + '\n'

    def get_next_record_pointer_as_string(self):
        if self.next_record_pointer is None:
            return self.fill_with("", '-', OVERFLOW_POINTER_SIZE)
        else:
            return self.fill_with(str(self.next_record_pointer), '0', OVERFLOW_POINTER_SIZE)

    def get_value_as_string(self):
        return self.fill_with(str(self.value), '0', RECORD_SIZE)

    @staticmethod
    def from_string(line, line_number=None):
        words = line.split(' ')
        key = words[0]
        if '.' in words[1]:
            value = float(words[1])
        else:
            value = int(words[1])

        if '-' in words[2]:
            overflow_pointer = None
        else:
            overflow_pointer = int(words[2])

        record = Record(key, value, overflow_pointer, line_number)
        return record

    @staticmethod
    def fill_with(base, char, overall_size):
        fill = char * (overall_size - len(base))
        return fill + base
