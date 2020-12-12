from .file_class import FileClass
from src.setup import *


class RecordFile(FileClass):
    LINE_SIZE = KEY_SIZE + len(' ') + RECORD_SIZE + len(' ') + OVERFLOW_POINTER_SIZE + len('\n') + 1

    def __init__(self, file_directory):
        super().__init__(file_directory)

    def update_record_pointer(self, record, new_pointer):
        offset = (record.line_number * self.LINE_SIZE) - (OVERFLOW_POINTER_SIZE + len('\n') + 1)
        self.update_pointer(offset, new_pointer)