from .record_file import RecordFile
from .elements import Record


class OverflowAreaFile(RecordFile):
    def __init__(self, file_directory):
        super().__init__(file_directory)

    def add_record(self, record, previous_record):
        save_line = self.size_in_lines
        if self.block is None or not self.block.if_line_buffered(save_line, check_length=False):
            page_number = int(save_line / self.BLOCK_SIZE_IN_LINES)
            self.read_block(page_number)
        record.set_line_number(save_line)
        self.block.append(record)
        self.size_in_lines += 1

    def find_record(self, key, starting_record):
        processing_record = starting_record
        while True:
            pointer = processing_record.get_next_record_pointer()
            if pointer is None:
                return False, processing_record

            previous_record = processing_record
            processing_record = self.read_record(pointer)

            if processing_record.key > key or processing_record.remove_flag == 1:
                return False, previous_record

            if processing_record.key == key:
                return True, processing_record

    def print_all(self):
        print("Overflow area")
        super(OverflowAreaFile, self).print_all()