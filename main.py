from src import AppCore

if __name__ == '__main__':
    app_core = AppCore()
    key = '012'
    record = app_core.read_record(key)
    print(record.value)
