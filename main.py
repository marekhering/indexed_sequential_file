from src import AppCore
from src.file_structures.elements.record import Record

if __name__ == '__main__':
    app_core = AppCore()
    key = '030'
    record = app_core.read_record(key)
    if record is None:
        print("None")
    else:
        print(record.value)

    new_record = Record('140', 4233)
    app_core.write_record(new_record)
