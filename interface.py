from src import AppCore
from src.file_structures.elements.record import Record
from src.setup import *

class Interface:
    def __init__(self):
        self.app_core = AppCore()
        self.test_file_path = "test"

    def run_menu(self):

        while True:

            print("Indexed sequential file")
            print("Options:")
            print("1. Read record")
            print("2. Insert record")
            print("3. Reorganize")
            print("4. Load test")
            # print("5. Clear input file")
            # print("6. Set new input file (" + self.input_directory + ")")
            print("0. Exit")
            print("Select an option number: ", end='')

            choice = input()

            print()

            if choice == '1':
                self.read_record()
            elif choice == '2':
                self.insert_record()
            elif choice == '3':
                self.add_records()
            elif choice == '4':
                self.load_test()
            # elif choice == '5':
            #     clear_file(self.input_directory)
            #     print("Input file cleared")
            #     print()
            # elif choice == '6':
            #     self.set_new_directory()
            # elif choice == '0':
            #     break
            else:
                print("Wrong option")
                print()

    def read_record(self):
        print("Enter record key: ", end='')
        key = input()
        if len(key) > KEY_SIZE:
            print("Wrong input")
            print()
            return
        try:
            key_as_int = int(key)
        except(ValueError, TypeError):
            print("Wrong input")
            print()
            return

        key = Record.fill_with(key, '0', KEY_SIZE)
        record = self.app_core.read_record(key)
        if record:
            print("Record value =", record.value)
        else:
            print("No record with given value")
        print()

    def load_test(self):
        with open(self.test_file_path, 'r') as file:
            for line in file:
                if not line:
                    break

                words = line[:-1].split(" ")
                instruction = words[0]
                if instruction == 'R':
                    key = Record.fill_with(words[1], '0', KEY_SIZE)
                    print("Read key " + key + " -> ", end='')
                    record = self.app_core.read_record(key)
                    if record:
                        print("Record value =", record.value)
                    else:
                        print("No record with given value")
        print()