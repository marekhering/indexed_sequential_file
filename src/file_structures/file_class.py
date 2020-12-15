from src.setup import *


class FileClass:
    LINE_SIZE = None
    BLANK_LINE = None
    BLOCK_SIZE_IN_LINES = None

    def __init__(self, file_directory):
        self.file_directory = file_directory
        self.size_in_lines = self.get_number_of_lines()
        self.block = None

    def get_number_of_lines(self):
        count = 0
        for _ in open(self.file_directory):
            count += 1
        return count

    def save_block(self, extend=False):
        if self.block is None:
            return False

        if extend:
            self.block.extend([None] * (self.BLOCK_SIZE_IN_LINES - len(self.block)))

        offset = self.block.first_line_number * (self.LINE_SIZE + 1)
        with open(self.file_directory, 'r+') as file:
            file.seek(offset)
            block_as_string = self.block.to_string(self.BLANK_LINE)
            file.write(block_as_string)

        return True