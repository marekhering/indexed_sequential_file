from .file_structures import *
from .file_structures.elements import Record
from src.setup import INDEXES_DIR, PRIMARY_AREA_DIR, OVERFLOW_AREA_DIR, FORCE_SAVE


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

    def browse(self):

        starting_key = self.index_file.indexes[0].key
        result_dict = self.find_record_in_files(starting_key)
        start_record = result_dict['record']
        base_primary_line = 0
        found_in_primary_area = True
        print("Line  Key  Value  Pointer  Area")
        while True:
            place_name = "PrimaryArea" if found_in_primary_area else "OverflowArea"
            print(str(start_record.get_number_of_lines()) + ' ' + start_record.to_string()[:-1] + ' ' + place_name)

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
            if next_line >= self.primary_area.size_in_lines:
                return None, False

            record = self.primary_area.read_record(next_line)
            if record is not None:
                return record, True

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

