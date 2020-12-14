from .file_class import FileClass
from src.setup import *
from .elements import Block, Record


class RecordFile(FileClass):
    LINE_SIZE = KEY_SIZE + len(' ') + RECORD_SIZE + len(' ') + OVERFLOW_POINTER_SIZE + len(' x') + len('\n')
    BLOCK_SIZE_IN_LINES = int(BLOCK_SIZE / LINE_SIZE)
    BLANK_LINE = '-' * (LINE_SIZE - 1)

    def __init__(self, file_directory):
        super().__init__(file_directory)
        self.read_successful = None

    def read_block(self, page_number, create_if_empty=False):
        first_line_number = page_number * self.BLOCK_SIZE_IN_LINES
        offset = first_line_number * (self.LINE_SIZE + 1)
        size = self.BLOCK_SIZE_IN_LINES * self.LINE_SIZE

        with open(self.file_directory, 'r') as file:
            file.seek(offset)
            block_as_string = file.read(size)

        new_block = Block.from_string(block_as_string, self.BLOCK_SIZE_IN_LINES, first_line_number, self.BLANK_LINE)
        if create_if_empty and not new_block:
            record_zero = Record(Record.fill_with('0', '0', KEY_SIZE), 0, remove_flag=1, line_number=0)
            new_block.append(record_zero)
            new_block.extend([None] * (self.BLOCK_SIZE_IN_LINES - 1))
            self.size_in_lines += self.BLOCK_SIZE_IN_LINES

        self.read_successful = False
        if len(new_block) != 0 or self.size_in_lines == 0:
            self.read_successful = True

        if self.block is not None:
            self.save_block()

        self.block = new_block

    def update_record_pointer(self, record, new_pointer):
        if not self.block.if_line_buffered(record.line_number):
            page_number = int(record.line_number / self.BLOCK_SIZE_IN_LINES)
            self.read_block(page_number)

        self.block.update_pointer(record.line_number, new_pointer)

    def update_record_remove_flag(self, record):
        if not self.block.if_line_buffered(record.line_number):
            page_number = int(record.line_number / self.BLOCK_SIZE_IN_LINES)
            self.read_block(page_number)

        self.block.update_remove_flag(record.line_number)

    def read_record(self, record_line_number):
        if self.block is None or not self.block.if_line_buffered(record_line_number):
            page_number = int(record_line_number / self.BLOCK_SIZE_IN_LINES)
            self.read_block(page_number)
        if self.read_successful:
            record = self.block.find_in_line(record_line_number)
        else:
            record = None
        return record

    def print_all(self):
        print("Line Key  Value Pointer  RemoveFlag")
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
