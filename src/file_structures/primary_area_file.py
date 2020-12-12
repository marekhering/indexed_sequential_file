from .record_file import RecordFile
from .overflow_area_file import OverflowAreaFile
from src.setup import *
from .elements import Record
from src.algorithms import bisection


class PrimaryAreaFile(RecordFile):
    def __init__(self, file_directory):
        super().__init__(file_directory)

    def find_record(self, key, starting_line, ending_line):
        block = self.read_block(starting_line, ending_line)
        keys = [record.get_key() for record in block]
        result, index_in_block = bisection(key, keys)
        record = block[index_in_block]
        return result, record

    def read_block(self, starting_line, ending_line):
        ending_line = self.size_in_lines + 1 if ending_line == 'EOF' else ending_line
        offset = (starting_line - 1) * self.LINE_SIZE
        size = (ending_line - starting_line) * (self.LINE_SIZE - 1)
        with open(self.file_directory, 'r') as file:
            file.seek(offset)
            block_as_string = file.read(size)

        lines_as_string = block_as_string.split('\n')
        block = []

        for i, line in enumerate(lines_as_string):
            if not line:
                break

            record = Record.from_string(line, line_number=(starting_line + i))
            block.append(record)

        return block
