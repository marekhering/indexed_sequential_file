from .record_file import RecordFile
from .elements import Record


class OverflowAreaFile(RecordFile):
    def __init__(self, file_directory):
        super().__init__(file_directory)

    def add_record(self, record, previous_record, counter_dict):
        save_line = self.size_in_lines
        if self.block is None or not self.block.if_line_buffered(save_line, check_length=False):
            page_number = int(save_line / self.BLOCK_SIZE_IN_LINES)
            saved = self.read_block(page_number)
            counter_dict['read_number'] += 1
            if saved:
                counter_dict['save_number'] += 1
        record.set_line_number(save_line)
        self.block.append(record)
        self.size_in_lines += 1

    def find_record(self, key, starting_record, counter_dict):
        processing_record = starting_record
        while True:
            pointer = processing_record.get_next_record_pointer()
            if pointer is None:
                return False, processing_record

            previous_record = processing_record
            processing_record = self.read_record(pointer, counter_dict)

            if processing_record.key > key:
                return False, previous_record

            if processing_record.key == key and processing_record.remove_flag == 0:
                return True, processing_record

    def print_all(self, counter_dict):
        print("Overflow area")
        super(OverflowAreaFile, self).print_all(counter_dict)