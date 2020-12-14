from .record_file import RecordFile


class PrimaryAreaFile(RecordFile):
    def __init__(self, file_directory):
        super().__init__(file_directory)

    def find_record(self, key, page_number, counter_dict):
        starting_line = page_number * self.BLOCK_SIZE_IN_LINES
        if self.block is None or starting_line != self.block.first_line_number:
            saved = self.read_block(page_number, create_if_empty=True)
            counter_dict['read_number'] += 1
            if saved:
                counter_dict['save_number'] += 1
        result, record = self.block.find_in_block(key)
        return result, record

    def add_record(self, record, previous_record, counter_dict):
        line_number = previous_record.line_number + 1
        record.set_line_number(line_number)
        self.block.add_record_in_line(record, line_number)

    def print_all(self, counter_dict):
        print("Primary area")
        super(PrimaryAreaFile, self).print_all(counter_dict)

