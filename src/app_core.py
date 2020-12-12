from .file_structures import *
from src.setup import INDEXES_DIR, PRIMARY_AREA_DIR, OVERFLOW_AREA_DIR


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

        self.overflow_area.add_record(new_record)
        previous_record_place.update_record_pointer(previous_record, self.overflow_area.size_in_lines)
        return True

    def find_record_in_files(self, key):
        result_dict = {
            'record': None,
            'found': False,
            'place': None
        }

        start_page_number, end_page_number = self.index_file.find_page_number(key)
        result, record_from_primary = self.primary_area.find_record(key, start_page_number, end_page_number)
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

