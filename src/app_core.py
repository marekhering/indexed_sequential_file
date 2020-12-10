from .file_structures import *
from src.setup import INDEXES_DIR, PRIMARY_AREA_DIR, OVERFLOW_AREA_DIR


class AppCore:
    def __init__(self):
        self.index_file = IndexFile(INDEXES_DIR)
        self.primary_area = PrimaryAreaFile(PRIMARY_AREA_DIR)
        self.overflow_area = OverflowAreaFile(OVERFLOW_AREA_DIR)

    def read_record(self, key):
        page_number = self.index_file.find_page_number(key)
        


