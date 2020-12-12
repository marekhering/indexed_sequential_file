from .record_file import RecordFile


class PrimaryAreaFile(RecordFile):
    def __init__(self, file_directory):
        super().__init__(file_directory)

    def find_record(self, key, page_number):
        result = False
        record = None
        if self.last_block is not None:
            result, record = self.last_block.find_in_block(key)

        if not result:
            self.read_block(page_number)
            result, record = self.last_block.find_in_block(key)

        return result, record

    def add_record(self, record, previous_record):
        result = self.last_block.find_place_after(previous_record)
        if result:
            line_number = previous_record.line_number + 1
            offset = line_number * (self.LINE_SIZE + 1)
            with open(self.file_directory, 'r+') as file:
                file.seek(offset)
                file.write(record.to_string())
        return result