from .record_file import RecordFile
from .elements import Record


class OverflowAreaFile(RecordFile):
    def __init__(self, file_directory):
        super().__init__(file_directory)

    def read_record(self, record_line_number):
        result = False
        record = None
        if self.last_block is not None:
            result, record = self.last_block.find_in_line(record_line_number)

        if not result:
            page_number = int(record_line_number / self.LINE_SIZE)
            self.read_block(page_number)
            result, record = self.last_block.find_in_line(record_line_number)

        return record

    def add_record(self, record):
        with open(self.file_directory, 'a') as file:
            file.write(record.to_string())
        self.size_in_lines += 1

    def find_record(self, key, starting_record):
        processing_record = starting_record
        while True:
            pointer = processing_record.get_next_record_pointer()
            if pointer is None:
                return False, processing_record

            previous_record = processing_record
            processing_record = self.read_record(pointer)

            if processing_record.key > key:
                return False, previous_record

            if processing_record.key == key:
                return True, processing_record
