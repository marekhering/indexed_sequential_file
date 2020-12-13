from .record_file import RecordFile


class PrimaryAreaFile(RecordFile):
    def __init__(self, file_directory):
        super().__init__(file_directory)

    def find_record(self, key, page_number):
        starting_line = page_number * self.BLOCK_SIZE_IN_LINES
        if self.block is None or starting_line != self.block.first_line_number:
            self.read_block(page_number, create_if_empty=True)

        result, record = self.block.find_in_block(key)
        return result, record

    def add_record(self, record, previous_record):
        line_number = previous_record.line_number + 1
        record.set_line_number(line_number)
        self.block.add_record_in_line(record, line_number)

    def print_all(self):
        print("Primary area")
        super(PrimaryAreaFile, self).print_all()

