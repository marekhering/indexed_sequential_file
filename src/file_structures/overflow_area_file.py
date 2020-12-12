from .record_file import RecordFile
from .elements import Record


class OverflowAreaFile(RecordFile):
    def __init__(self, file_directory):
        super().__init__(file_directory)

    def read_record(self, record_line_number):
        offset = (record_line_number - 1) * self.LINE_SIZE
        with open(self.file_directory, 'r') as file:
            file.seek(offset)
            line = file.read(self.LINE_SIZE - 1)

        record = Record.from_string(line, line_number=record_line_number)
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
