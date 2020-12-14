from src import AppCore
from src.file_structures.elements.record import Record
from src.setup import *


class Interface:
    def __init__(self):
        self.app_core = AppCore()
        self.test_file_path = "test"
        self.total_counter = {
            'total_save': 0,
            'total_read': 0
        }

    def run_menu(self):

        while True:

            print("Indexed sequential file")
            print("Options:")
            print("1. Read record")
            print("2. Insert record")
            print("3. Remove record")
            print("4. Update record")
            print("5. Browse")
            print("6. Reorganize")
            print("7. Load test")
            print("8. Clear files")
            print("0. Exit")
            print("Select an option number: ", end='')

            choice = input()

            print()

            if choice == '1':
                self.read_record()
            elif choice == '2':
                self.insert_record()
            elif choice == '3':
                self.remove_record()
            elif choice == '4':
                self.update_record()
            elif choice == '5':
                self.browse()
            elif choice == '6':
                self.reorganize()
            elif choice == '7':
                self.load_test()
            elif choice == '8':
                self.app_core.clear_files()
            elif choice == '0':
                counter = self.app_core.save_all()
                self.add_to_counter(counter)
                print()
                print("Total number of reads", self.total_counter['total_read'])
                print("Total number of saves", self.total_counter['total_save'], '\n')
                break
            else:
                print("Wrong option")
                print()

    def read_record(self):
        print("Read record")
        key = self.insert_key()
        if key is None:
            return
        record, counter_dict = self.app_core.read_record(key)
        if record:
            print("Record value =", record.value)
        else:
            print("No record with given key")
        print()
        print("Number of reads", counter_dict['read_number'])
        print("Number of saves", counter_dict['save_number'], '\n')
        self.add_to_counter(counter_dict)
        return counter_dict

    def insert_record(self):
        print("Insert record")
        key = self.insert_key()
        value = self.insert_value()
        if key is None or value is None:
            return
        record = Record(key, value)
        result, counter_dict = self.app_core.write_record(record)
        if result:
            print("Record inserted")
        else:
            print("Record already exist")
        print()
        print()
        print("Number of reads", counter_dict['read_number'])
        print("Number of saves", counter_dict['save_number'], '\n')
        self.add_to_counter(counter_dict)

    def remove_record(self):
        print("Remove record")
        key = self.insert_key()
        if key is None:
            return
        result, counter_dict = self.app_core.remove_record(key)
        if result:
            print("Record removed")
        else:
            print("No record with given key")
        print()
        print("Number of reads", counter_dict['read_number'])
        print("Number of saves", counter_dict['save_number'], '\n')
        self.add_to_counter(counter_dict)

    def update_record(self):
        print("Update record")
        key = self.insert_key()
        new_value = self.insert_value()
        if key is None or new_value is None:
            return
        result, counter_dict = self.app_core.update_record(key, new_value)
        if result:
            print("Record updated")
        else:
            print("No record with given key")
        print()
        print()
        print("Number of reads", counter_dict['read_number'])
        print("Number of saves", counter_dict['save_number'], '\n')
        self.add_to_counter(counter_dict)

    def browse(self):
        print("Browse option: ")
        print("1. Print records in files")
        print("2. Print records as chain")
        print("Enter browse option: ", end='')
        option = input()
        print()
        if option == '1':
            counter_dict = self.app_core.print_flies()
        elif option == '2':
            counter_dict = self.app_core.browse()
        else:
            print("Wrong option")
            print()
            return
        print()
        print("Number of reads", counter_dict['read_number'])
        print("Number of saves", counter_dict['save_number'], '\n')
        self.add_to_counter(counter_dict)

    def reorganize(self):
        counter_dict = self.app_core.reorganize()
        print("File reorganized")
        print()
        print("Number of reads", counter_dict['read_number'])
        print("Number of saves", counter_dict['save_number'], '\n')
        self.add_to_counter(counter_dict)

    def load_test(self):
        test_counter_dict = {
            'read_number': 0,
            'save_number': 0
        }

        with open(self.test_file_path, 'r') as file:
            for line in file:
                if not line:
                    break
                counter_dict = 0
                words = line[:-1].split(" ")
                instruction = words[0]
                if instruction == 'R':
                    key = Record.fill_with(words[1], '0', KEY_SIZE)
                    print("Read record with key " + key + " -> ", end='')
                    record, counter_dict = self.app_core.read_record(key)
                    if record:
                        print("Record value =", record.value)
                    else:
                        print("No record with given key")

                if instruction == 'W':
                    key = Record.fill_with(words[1], '0', KEY_SIZE)
                    value = float(words[2]) if '.' in words[2] else int(words[2])
                    print("Write record with key " + key + " and value " + str(value) + " -> ", end='')
                    record = Record(key, value)
                    result, counter_dict = self.app_core.write_record(record)
                    if result:
                        print("Record inserted")
                    else:
                        print("Record already exist")

                if counter_dict is not None:
                    test_counter_dict['read_number'] += counter_dict['read_number']
                    test_counter_dict['save_number'] += counter_dict['save_number']
        print()
        print("Number of reads", test_counter_dict['read_number'])
        print("Number of saves", test_counter_dict['save_number'], '\n')

    def add_to_counter(self, counter):
        self.total_counter['total_read'] += counter['read_number']
        self.total_counter['total_save'] += counter['save_number']

    @staticmethod
    def insert_key():
        print("Enter record key: ", end='')
        key = input()
        if len(key) > KEY_SIZE:
            print("Wrong input")
            print()
            return None
        try:
            key_as_int = int(key)
        except(ValueError, TypeError):
            print("Wrong input")
            print()
            return None
        key = Record.fill_with(key, '0', KEY_SIZE)
        return key

    @staticmethod
    def insert_value():
        print("Enter record value: ", end='')
        value = input()
        if len(value) > RECORD_SIZE:
            print("Wrong input")
            print()
            return None
        try:
            numerical_value = float(value) if '.' in value else int(value)
        except(ValueError, TypeError):
            print("Wrong input")
            print()
            return None

        return numerical_value

