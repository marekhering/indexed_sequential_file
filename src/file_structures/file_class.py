from src.setup import *


class FileClass:
    def __init__(self, file_directory):
        self.file_directory = file_directory
        self.size_in_lines = self.get_number_of_lines()

    def get_number_of_lines(self):
        count = 0
        for _ in open(self.file_directory):
            count += 1
        return count

    def update_pointer(self, offset, new_value):
        new_value = str(new_value)
        zeros = '0' * (OVERFLOW_POINTER_SIZE - len(new_value))
        new_value = zeros + new_value
        with open(self.file_directory, 'r+') as file:
            file.seek(offset)
            file.write(new_value)
