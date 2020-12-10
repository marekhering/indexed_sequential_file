from src import AppCore

if __name__ == '__main__':
    app_core = AppCore()
    key = '034'
    value = app_core.read_record(key)
    print(value)