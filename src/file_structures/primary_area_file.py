from .file_class import FileClass
from .overflow_area_file import OverflowAreaFile
from src.setup import *
from .elements import Record
from src.algorithms import bisection

class PrimaryAreaFile(FileClass):
    LINE_SIZE = KEY_SIZE + len(' ') + RECORD_SIZE + len(' ') + OVERFLOW_POINTER_SIZE + len('\n')

    def __init__(self, file_directory):
        super().__init__(file_directory)
        self.overflow_area = OverflowAreaFile(OVERFLOW_AREA_DIR)

    def find_record(self, key, starting_line, ending_line):
        block = self.read_block(starting_line, ending_line)
        keys = [record.get_key() for record in block]
        index = bisection(key, keys)
        record = block[index]
        return record

    def read_block(self, starting_line, ending_line):
        offset = (starting_line - 1) * (self.LINE_SIZE + 1)
        size = (ending_line - starting_line) * self.LINE_SIZE
        with open(self.file_directory, 'r') as file:
            file.seek(offset)
            block_as_string = file.read(size)

        lines_as_string = block_as_string.split('\n')
        block = []

        for lines_as_string in lines_as_string:
            if not lines_as_string:
                break
            line = lines_as_string.split(' ')
            key = line[0]
            if '.' in line[1]:
                value = float(line[1])
            else:
                value = int(line[1])

            if 'N' in line[2]:
                overflow_pointer = None
            else:
                overflow_pointer = int(line[2])

            record = Record(key, value, overflow_pointer)
            block.append(record)

        return block


