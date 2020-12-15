from .file_structures import *
from .file_structures.elements import Block, Index, Record
from src.setup import INDEXES_DIR, PRIMARY_AREA_DIR, OVERFLOW_AREA_DIR, FORCE_SAVE, ALPHA, KEY_SIZE, AUTO_REORGANIZATION
import os


class AppCore:
    def __init__(self):
        self.index_file = IndexFile(INDEXES_DIR)
        self.primary_area = PrimaryAreaFile(PRIMARY_AREA_DIR)
        self.overflow_area = OverflowAreaFile(OVERFLOW_AREA_DIR)

    def read_record(self, key):
        counter_dict = {
            'read_number': 0,
            'save_number': 0
        }
        result_dict = self.find_record_in_files(key, counter_dict)
        if result_dict['found']:
            return result_dict['record'], counter_dict
        else:
            return None, counter_dict

    def write_record(self, new_record):
        counter_dict = {
            'read_number': 0,
            'save_number': 0
        }
        new_record_key = new_record.get_key()
        result_dict = self.find_record_in_files(new_record_key, counter_dict)
        if result_dict['found']:
            return False, counter_dict

        previous_record = result_dict['record']
        previous_record_place = result_dict['place']

        new_record.set_next_record_pointer(previous_record.get_next_record_pointer())

        next_record_place = self.overflow_area
        if previous_record_place == self.primary_area:
            if self.primary_area.block.find_place_after(previous_record):
                next_record_place = self.primary_area

        next_record_place.add_record(new_record, previous_record, counter_dict)

        if next_record_place == self.overflow_area:
            previous_record_place.update_record_pointer(previous_record, self.overflow_area.size_in_lines - 1, counter_dict)

        if FORCE_SAVE and (next_record_place == self.overflow_area or previous_record_place == self.overflow_area):
            self.overflow_area.save_block()

        if FORCE_SAVE and (next_record_place == self.primary_area or previous_record_place == self.primary_area):
            self.primary_area.save_block()

        if self.overflow_area.size_in_lines > self.primary_area.size_in_lines * AUTO_REORGANIZATION:
            print(" --Auto reorganization-- ", end='')
            reorganize_dict = self.reorganize()
            counter_dict['read_number'] += reorganize_dict['read_number']
            counter_dict['save_number'] += reorganize_dict['save_number']
        place_name = "Primary Area" if next_record_place == self.primary_area else "Overflow Area"
        print("Record inserted in", new_record.get_line_number(), "line of", place_name)

        return True, counter_dict

    def update_record(self, key, new_value):
        counter_dict = {
            'read_number': 0,
            'save_number': 0
        }
        result_dict = self.find_record_in_files(key, counter_dict)
        if not result_dict['found']:
            return False, counter_dict
        result_dict['place'].update_record_value(result_dict['record'], new_value, counter_dict)
        if FORCE_SAVE:
            result_dict['place'].save_block()

        return True, counter_dict

    def print_flies(self):
        counter_dict = {
            'read_number': 0,
            'save_number': 0
        }
        self.index_file.print_all()
        self.primary_area.print_all(counter_dict)
        self.overflow_area.print_all(counter_dict)
        return counter_dict

    def save_all(self):
        counter_dict = {
            'read_number': 0,
            'save_number': 0
        }
        if self.primary_area.save_block():
            counter_dict['save_number'] += 1
        if self.overflow_area.save_block():
            counter_dict['save_number'] += 1
        return counter_dict

    def browse(self):
        counter_dict = {
            'read_number': 0,
            'save_number': 0
        }
        starting_key = self.index_file.indexes[0].key
        result_dict = self.find_record_in_files(starting_key, counter_dict)
        start_record = result_dict['record']
        base_primary_line = 0
        jump = 1
        found_in_primary_area = True
        print("Area     Line Key  Value     Pointer RemoveFlag")
        while True:
            place_name = "PrimaryArea" if found_in_primary_area else "OverflowArea"
            print(place_name + ' ' + str(start_record.get_line_number()) + ' ' + start_record.to_string()[:-1], end='')
            if jump > 1:
                print(" (" + str(jump - 1) + " free space)")
            else:
                print("")

            next_record, found_in_primary_area, jump = self.find_next_record(start_record, base_primary_line, counter_dict)
            if found_in_primary_area:
                base_primary_line = next_record.get_line_number()
            if next_record is None:
                break
            start_record = next_record
        print()
        return counter_dict

    def find_next_record(self, previous_record, base_primary_line, counter_dict):
        pointer = previous_record.get_next_record_pointer()
        if pointer is not None:
            record = self.overflow_area.read_record(pointer, counter_dict)
            return record, False, 0

        next_line = base_primary_line
        while True:
            next_line = next_line + 1
            if self.primary_area.read_successful is not None and self.primary_area.read_successful is False:
                return None, False, 0

            record = self.primary_area.read_record(next_line, counter_dict)
            if record is not None:
                jump = record.get_line_number() - base_primary_line
                return record, True, jump

    def remove_record(self, key):
        counter_dict = {
            'read_number': 0,
            'save_number': 0
        }
        result_dict = self.find_record_in_files(key, counter_dict)
        if result_dict['found']:
            result_dict['place'].update_record_remove_flag(result_dict['record'], counter_dict)
            if FORCE_SAVE:
                result_dict['place'].save_block()
            return True, counter_dict
        else:
            return False, counter_dict

    def find_record_in_files(self, key, counter_dict):
        result_dict = {
            'record': None,
            'found': False,
            'place': None
        }

        page_number = self.index_file.find_page_number(key)
        result, record_from_primary = self.primary_area.find_record(key, page_number, counter_dict)
        if result is True:
            result_dict['record'] = record_from_primary
            result_dict['found'] = True
            result_dict['place'] = self.primary_area
            return result_dict

        record_from_overflow = record_from_primary
        if key > record_from_primary.get_key():
            result, record_from_overflow = self.overflow_area.find_record(key, record_from_primary, counter_dict)
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

    def clear_files(self):
        create_temp_file(INDEXES_DIR)
        create_temp_file(PRIMARY_AREA_DIR)
        create_temp_file(OVERFLOW_AREA_DIR)
        self.index_file = IndexFile(INDEXES_DIR)
        self.primary_area = PrimaryAreaFile(PRIMARY_AREA_DIR)
        self.overflow_area = OverflowAreaFile(OVERFLOW_AREA_DIR)

    def reorganize(self):
        counter_dict = {
            'read_number': 0,
            'save_number': 0
        }

        starting_key = self.index_file.indexes[0].key
        result_dict = self.find_record_in_files(starting_key, counter_dict)
        start_record = result_dict['record']
        base_primary_line = 0
        base_save_primary_line = 0
        page_number = 0
        run = True

        create_temp_file(INDEXES_DIR + "_temp")
        create_temp_file(PRIMARY_AREA_DIR + "_temp")
        create_temp_file(OVERFLOW_AREA_DIR + "_temp")

        new_index_file = IndexFile(INDEXES_DIR + "_temp")
        new_primary_file = PrimaryAreaFile(PRIMARY_AREA_DIR + "_temp")

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
                                ((number_of_records - number_of_records_in_block) + 000.1))

        while run:
            record_jump -= 1

            next_record = None
            if counter == 0 or record_jump == 0:
                next_record, found_in_primary, jump = self.find_next_record(start_record, base_primary_line, counter_dict)

                if next_record is None:
                    run = False

                if run:
                    if found_in_primary:
                        base_primary_line += jump

                    start_record = next_record.copy()

                    if next_record.remove_flag == 1:
                        record_jump = 1
                        continue

                    record_jump = 1 + round((number_of_empty_records - number_of_empty_records_in_block) /
                                            ((number_of_records - number_of_records_in_block) + 000.1))

                    if counter == 0:
                        new_index = Index(next_record.get_key(), page_number)
                        reorganize_index_block.append(new_index)
                    next_record.set_next_record_pointer(None)
                    next_record.set_line_number(base_save_primary_line + counter)
                    number_of_records_in_block += 1
            else:
                number_of_empty_records_in_block += 1

            if run:
                reorganize_primary_block.append(next_record)
                counter += 1

            if reorganize_primary_block.is_full() or run is False:
                new_primary_file.block = reorganize_primary_block
                new_primary_file.save_block(extend=True)
                counter_dict['save_number'] += 1
                base_save_primary_line += counter
                counter = 0
                page_number += 1
                reorganize_primary_block = Block(base_save_primary_line, self.primary_area.BLOCK_SIZE_IN_LINES)
                number_of_records_in_block = 0
                number_of_empty_records_in_block = 0

            if reorganize_index_block.is_full() or run is False:
                new_index_file.block = reorganize_index_block
                new_index_file.save_block()
                counter_dict['save_number'] += 1
                reorganize_index_block = Block(page_number, self.index_file.BLOCK_SIZE_IN_LINES)

        os.remove(INDEXES_DIR)
        os.remove(PRIMARY_AREA_DIR)
        os.remove(OVERFLOW_AREA_DIR)

        os.rename(INDEXES_DIR + "_temp", INDEXES_DIR)
        os.rename(PRIMARY_AREA_DIR + "_temp", PRIMARY_AREA_DIR)
        os.rename(OVERFLOW_AREA_DIR + "_temp", OVERFLOW_AREA_DIR)

        self.index_file = IndexFile(INDEXES_DIR)
        self.primary_area = PrimaryAreaFile(PRIMARY_AREA_DIR)
        self.overflow_area = OverflowAreaFile(OVERFLOW_AREA_DIR)

        return counter_dict


def create_temp_file(path):
    with open(path, "w"):
        pass
