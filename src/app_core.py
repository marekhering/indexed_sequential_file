from .file_structures import *
from .file_structures.elements import Block, Index, Record
from src.setup import INDEXES_DIR, PRIMARY_AREA_DIR, OVERFLOW_AREA_DIR, FORCE_SAVE, ALPHA, KEY_SIZE


class AppCore:
    def __init__(self):
        self.index_file = IndexFile(INDEXES_DIR)
        self.primary_area = PrimaryAreaFile(PRIMARY_AREA_DIR)
        self.overflow_area = OverflowAreaFile(OVERFLOW_AREA_DIR)

    def read_record(self, key):
        result_dict = self.find_record_in_files(key)
        if result_dict['found']:
            return result_dict['record']
        else:
            return None

    def write_record(self, new_record):
        new_record_key = new_record.get_key()
        result_dict = self.find_record_in_files(new_record_key)
        if result_dict['found']:
            return False

        previous_record = result_dict['record']
        previous_record_place = result_dict['place']

        new_record.set_next_record_pointer(previous_record.get_next_record_pointer())

        next_record_place = self.overflow_area
        if previous_record_place == self.primary_area:
            if self.primary_area.block.find_place_after(previous_record):
                next_record_place = self.primary_area

        next_record_place.add_record(new_record, previous_record)

        if next_record_place == self.overflow_area:
            previous_record_place.update_record_pointer(previous_record, self.overflow_area.size_in_lines - 1)

        if FORCE_SAVE and (next_record_place == self.overflow_area or previous_record_place == self.overflow_area):
            self.overflow_area.save_block()

        if FORCE_SAVE and (next_record_place == self.primary_area or previous_record_place == self.primary_area):
            self.primary_area.save_block()

        return True

    def print_flies(self):
        self.index_file.print_all()
        self.primary_area.print_all()
        self.overflow_area.print_all()

    def save_all(self):
        self.index_file.save_block()
        self.primary_area.save_block()
        self.overflow_area.save_block()

    def browse(self):

        starting_key = self.index_file.indexes[0].key
        result_dict = self.find_record_in_files(starting_key)
        start_record = result_dict['record']
        base_primary_line = 0
        found_in_primary_area = True
        print("Area     Line Key  Value     Pointer RemoveFlag")
        while True:
            place_name = "PrimaryArea" if found_in_primary_area else "OverflowArea"
            print(place_name + ' ' + str(start_record.get_line_number()) + ' ' + start_record.to_string()[:-1])

            next_record, found_in_primary_area = self.find_next_record(start_record, base_primary_line)
            if found_in_primary_area:
                base_primary_line = next_record.get_line_number()
            if next_record is None:
                break
            start_record = next_record
        print()

    def find_next_record(self, previous_record, base_primary_line):
        pointer = previous_record.get_next_record_pointer()
        if pointer is not None:
            record = self.overflow_area.read_record(pointer)
            return record, False

        next_line = base_primary_line
        while True:
            next_line = next_line + 1
            if self.primary_area.read_successful is not None and self.primary_area.read_successful is False:
                return None, False

            record = self.primary_area.read_record(next_line)
            if record is not None:
                return record, True

    def remove_record(self, key):
        result_dict = self.find_record_in_files(key)
        if result_dict['found']:
            result_dict['place'].update_record_remove_flag(result_dict['record'])
            if FORCE_SAVE:
                result_dict['place'].primary_area.save_block()
            return True
        else:
            return False

    def find_record_in_files(self, key):
        result_dict = {
            'record': None,
            'found': False,
            'place': None
        }

        page_number = self.index_file.find_page_number(key)
        result, record_from_primary = self.primary_area.find_record(key, page_number)
        if result is True:
            result_dict['record'] = record_from_primary
            result_dict['found'] = True
            result_dict['place'] = self.primary_area
            return result_dict

        record_from_overflow = record_from_primary
        if key > record_from_primary.get_key():
            result, record_from_overflow = self.overflow_area.find_record(key, record_from_primary)
            if result is True:
                result_dict['record'] = record_from_overflow
                result_dict['found'] = True
                result_dict['place'] = self.overflow_area
                return result_dict

        result_dict['found'] = False
        result_dict['record'] = record_from_overflow
        if record_from_overflow == record_from_primary:
            result_dict['place'] = self.primary_area
        else:
            result_dict['place'] = self.overflow_area

        return result_dict

    def reorganize(self):

        starting_key = self.index_file.indexes[0].key
        result_dict = self.find_record_in_files(starting_key)
        start_record = result_dict['record']
        base_primary_line = 0
        base_save_primary_line = 0
        page_number = 0
        empty_records = 0
        run = True

        create_temp_file(INDEXES_DIR + "_temp")
        create_temp_file(PRIMARY_AREA_DIR + "_temp")
        create_temp_file(OVERFLOW_AREA_DIR + "_temp")

        new_index_file = IndexFile(INDEXES_DIR + "_temp")
        new_primary_file = PrimaryAreaFile(PRIMARY_AREA_DIR + "_temp")
        new_overflow_file = OverflowAreaFile(OVERFLOW_AREA_DIR + "_temp")

        reorganize_index_block = Block(page_number, self.index_file.BLOCK_SIZE_IN_LINES)
        reorganize_primary_block = Block(base_primary_line, self.primary_area.BLOCK_SIZE_IN_LINES)

        number_of_empty_records = int(self.primary_area.BLOCK_SIZE_IN_LINES * ALPHA)
        number_of_records = self.primary_area.BLOCK_SIZE_IN_LINES - number_of_empty_records

        zero_index = Index('0' * KEY_SIZE, '0')
        zero_record = Record('0' * KEY_SIZE, 0, remove_flag=1, line_number=0)
        reorganize_index_block.append(zero_index)
        reorganize_primary_block.append(zero_record)
        counter = 1

        number_of_records_in_block = 1
        number_of_empty_records_in_block = 0
        record_jump = 1 + round((number_of_empty_records - number_of_empty_records_in_block) /
                                (number_of_records - number_of_records_in_block) + 000.1)

        while run:
            record_jump -= 1

            next_record = None
            if counter == 0 or record_jump == 0:
                record_jump = 1 + round((number_of_empty_records - number_of_empty_records_in_block) /
                                        (number_of_records - number_of_records_in_block) + 000.1)
                next_record, found_in_primary = self.find_next_record(start_record, base_primary_line)
                if found_in_primary:
                    base_primary_line += 1

                if next_record is None:
                    run = False
                else:
                    start_record = next_record.copy()
                    if counter == 0:
                        new_index = Index(next_record.get_key(), page_number)
                        reorganize_index_block.append(new_index)
                    next_record.set_next_record_pointer(None)
                    next_record.set_line_number(base_save_primary_line + counter)
                    number_of_records_in_block += 1
            else:
                number_of_empty_records_in_block += 1

            if run and (next_record is None or next_record.remove_flag == 0):
                reorganize_primary_block.append(next_record)
                counter += 1

            if reorganize_primary_block.is_full() or run is False:
                new_primary_file.block = reorganize_primary_block
                new_primary_file.save_block(extend=True)
                base_save_primary_line += counter
                counter = 0
                empty_records = 0
                page_number += 1
                reorganize_primary_block = Block(base_save_primary_line, self.primary_area.BLOCK_SIZE_IN_LINES)
                number_of_records_in_block = 0
                number_of_empty_records_in_block = 0

            if reorganize_index_block.is_full() or run is False:
                new_index_file.block = reorganize_index_block
                new_index_file.save_block()

        

def create_temp_file(path):
    with open(path, "w"):
        pass
