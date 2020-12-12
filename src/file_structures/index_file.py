from .file_class import FileClass
from src.algorithms import bisection
from src.file_structures.elements.index import Index
from src.setup import *


class IndexFile(FileClass):
    def __init__(self, file_directory):
        super().__init__(file_directory)
        self.indexes = IndexFile.read_index_file(file_directory)

    def find_page_number(self, key):
        _, index = bisection(key, self.get_index_keys())
        page_number = self.indexes[index].get_page_number()
        return page_number

    def get_index_keys(self):
        return [index.get_key() for index in self.indexes]

    @staticmethod
    def read_index_file(file_directory):
        index_list = list()
        with open(file_directory, 'r') as file:
            for line in file.readlines():
                words = line.split(' ')
                index = Index(words[0], words[1][:-1])
                index_list.append(index)

        if not index_list:
            key = '0' * KEY_SIZE
            page_number = '0' * PAGE_NUMBER_SIZE
            zero_index = Index(key, page_number)
            index_list.append(zero_index)

        return index_list

