from .file_class import FileClass
from src.setup import *
from .elements import Block, Record


class RecordFile(FileClass):
    LINE_SIZE = KEY_SIZE + len(' ') + RECORD_SIZE + len(' ') + OVERFLOW_POINTER_SIZE + len('\n')
    BLOCK_SIZE_IN_LINES = int(BLOCK_SIZE / LINE_SIZE)
    BLANK_LINE = '-' * (LINE_SIZE - 1)

    def __init__(self, file_directory):
        super().__init__(file_directory)
        self.block = None

    def read_block(self, page_number, create_if_empty=False):
        first_line_number = page_number * self.BLOCK_SIZE_IN_LINES
        offset = first_line_number * (self.LINE_SIZE + 1)
        size = self.BLOCK_SIZE_IN_LINES * self.LINE_SIZE

        with open(self.file_directory, 'r') as file:
            file.seek(offset)
            block_as_string = file.read(size)

        block = Block.from_string(block_as_string, self.BLOCK_SIZE_IN_LINES, first_line_number, self.BLANK_LINE)
        if create_if_empty and not block:
            record_zero = Record(Record.fill_with('0', '0', KEY_SIZE), 0)
            record_zero.set_line_number(0)
            block.append(record_zero)
            block.extend([None] * (self.BLOCK_SIZE_IN_LINES - 1))

        if self.block is not None:
            self.save_block()

        self.block = block

    def save_block(self):
        offset = self.block.first_line_number * (self.LINE_SIZE + 1)
        with open(self.file_directory, 'r+') as file:
            file.seek(offset)
            block_as_string = self.block.to_string(self.BLANK_LINE)
            file.write(block_as_string)

    def update_record_pointer(self, record, new_pointer):
        if self.block.if_line_buffered(record.line_number):
            self.block.update_pointer(record.line_number, new_pointer)
        else:
            page_number = int(record.line_number / self.BLOCK_SIZE_IN_LINES)
            self.read_block(page_number)
            self.block.update_pointer(record.line_number, new_pointer)

    def read_record(self, record_line_number):
        if self.block is None or not self.block.if_line_buffered(record_line_number):
            page_number = int(record_line_number / self.BLOCK_SIZE_IN_LINES)
            self.read_block(page_number)

        record = self.block.find_in_line(record_line_number)
        return record

    def print_all(self):
        print("Line Key  Value Pointer")
        line_number = 0
        while True:
            if self.block is None or not self.block.if_line_buffered(line_number):
                page_number = int(line_number / self.BLOCK_SIZE_IN_LINES)
                self.read_block(page_number)

            if not self.block.if_line_buffered(line_number):
                break
            record = self.block.find_in_line(line_number)
            if not record:
                record = self.BLANK_LINE + '\n'
            else:
                record = record.to_string()
            print(str(line_number) + " " + record, end='')
            line_number += 1
        print()
