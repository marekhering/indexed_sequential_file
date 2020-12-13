from .record import Record
from src.algorithms import bisection
from src.setup import *


class Block(list):

    def __init__(self, first_line_number, max_size):
        super().__init__()
        self.max_size = max_size
        self.first_line_number = first_line_number

    def find_in_block(self, key):
        records = self.get_records()
        keys = [record.get_key() for record in records]
        result, index = bisection(key, keys)
        record = records[index]
        return result, record

    def find_place_after(self, record):
        index = self.index(record)
        if index != len(self) - 1 and self[index + 1] is None:
            return True
        else:
            return False

    def find_in_line(self, line_number):
        index = line_number - self.first_line_number
        return self[index]

    def add_record_in_line(self, record, line_number):
        index = line_number - self.first_line_number
        self[index] = record

    def append(self, record):
        if len(self) >= self.max_size:
            print("Cannot append")
            return
        super(Block, self).append(record)

    def update_pointer(self, line_number, new_pointer):
        index = line_number - self.first_line_number
        self[index].set_next_record_pointer(new_pointer)

    def get_records(self):
        return [record for record in self if record is not None]

    def if_line_buffered(self, line_number):
        result = True if self.first_line_number <= line_number < self.first_line_number + self.max_size else False
        if line_number >= self.first_line_number + len(self):
            result = False
        return result

    def to_string(self, blank_line):
        block_as_string = ""
        for record in self:
            if record is not None:
                block_as_string += record.to_string()
            else:
                block_as_string += blank_line + '\n'
        return block_as_string

    @staticmethod
    def from_string(block_as_string, block_size, first_line_number, blank_line):
        lines_as_string = block_as_string.split('\n')
        block = Block(first_line_number, block_size)
        for i, line in enumerate(lines_as_string):
            if not line:
                break

            if line == blank_line:
                record = None
            else:
                record = Record.from_string(line, line_number=(first_line_number + i))

            block.append(record)

        return block
