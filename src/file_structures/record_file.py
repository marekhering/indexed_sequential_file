from .file_class import FileClass
from src.setup import *
from .elements import Block


class RecordFile(FileClass):
    LINE_SIZE = KEY_SIZE + len(' ') + RECORD_SIZE + len(' ') + OVERFLOW_POINTER_SIZE + len('\n')
    BLOCK_SIZE_IN_LINES = int(BLOCK_SIZE / LINE_SIZE)
    BLANK_LINE = '-' * (LINE_SIZE - 1)

    def __init__(self, file_directory):
        super().__init__(file_directory)
        self.last_block = None

    def read_block(self, page_number):
        first_line_number = page_number * self.BLOCK_SIZE_IN_LINES
        offset = first_line_number * (self.LINE_SIZE + 1)
        size = self.BLOCK_SIZE_IN_LINES * self.LINE_SIZE

        with open(self.file_directory, 'r') as file:
            file.seek(offset)
            block_as_string = file.read(size)

        block = Block.from_string(block_as_string, first_line_number, self.BLANK_LINE)
        self.last_block = block

    def update_record_pointer(self, record, new_pointer):
        offset = record.line_number * (self.LINE_SIZE + 1) + KEY_SIZE + len(' ') + RECORD_SIZE + len(' ')
        self.update_pointer(offset, new_pointer)