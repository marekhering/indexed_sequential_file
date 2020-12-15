from .file_class import FileClass
from src.algorithms import bisection
from .elements import Index, Block
from src.setup import *


class IndexFile(FileClass):
    LINE_SIZE = KEY_SIZE + len(' ') + PAGE_NUMBER_SIZE + len('\n')
    BLOCK_SIZE_IN_LINES = int(BLOCK_SIZE / LINE_SIZE)
    BLANK_LINE = '-' * (LINE_SIZE - 1)

    def __init__(self, file_directory):
        super().__init__(file_directory)
        self.indexes = []

    def find_page_number(self, key):
        if len(self.indexes) == 0:
            self.indexes.extend(self.read_index_file())
        _, index = bisection(key, self.get_index_keys())
        page_number = self.indexes[index].get_page_number()
        return page_number

    def get_index_keys(self):
        return [index.get_key() for index in self.indexes]

    def print_all(self):
        print("Index file")
        print("Key  PageNumber")
        for index in self.indexes:
            print(index.to_string(), end='')
        print()

    def read_block(self, page_number, create_if_empty=False):
        first_line_number = page_number * self.BLOCK_SIZE_IN_LINES
        offset = first_line_number * (self.LINE_SIZE + 1)
        size = self.BLOCK_SIZE_IN_LINES * self.LINE_SIZE

        with open(self.file_directory, 'r') as file:
            file.seek(offset)
            block_as_string = file.read(size)

        new_block = Block.from_string_index(block_as_string, self.BLOCK_SIZE_IN_LINES, first_line_number, self.BLANK_LINE)
        if create_if_empty and not new_block and self.size_in_lines == 0:
            key = '0' * KEY_SIZE
            page_number = '0' * PAGE_NUMBER_SIZE
            zero_index = Index(key, page_number)
            self.indexes.append(zero_index)


        self.read_successful = False
        if len(new_block) != 0 or self.size_in_lines == 0:
            self.read_successful = True

        saved = False
        if self.block is not None and self.block.change_flag:
            self.save_block()
            saved = True

        self.block = new_block
        return saved

    def read_index_file(self):
        index_list = []
        start_page_number = 0
        while True:
            self.read_block(start_page_number)
            if not self.block:
                break
            start_page_number += 1
            for index in self.block:
                index_list.append(index)
                self.size_in_lines += 1

        if start_page_number == 0:
            self.read_block(0, create_if_empty=True)
        return index_list

