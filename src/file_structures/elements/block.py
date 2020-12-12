from .record import Record
from src.algorithms import bisection


class Block(list):
    def __init__(self, first_line_number):
        super().__init__()
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

    def get_records(self):
        return [record for record in self if record is not None]

    @staticmethod
    def from_string(block_as_string, first_line_number, blank_line):
        lines_as_string = block_as_string.split('\n')
        block = Block(first_line_number)
        for i, line in enumerate(lines_as_string):
            if not line:
                break

            if line == blank_line:
                record = None
            else:
                record = Record.from_string(line, line_number=(first_line_number + i))

            block.append(record)

        return block
