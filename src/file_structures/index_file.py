from .file_class import FileClass
from src.algorithms import bisection
from src.file_structures.elements.index import Index


class IndexFile(FileClass):
    def __init__(self, file_directory):
        super().__init__(file_directory)
        self.indexes = IndexFile.read_index_file(file_directory)

    def find_page_number(self, key):
        _, index = bisection(key, self.get_index_keys())
        start_page_number = int(self.indexes[index].get_page_number())
        if index != len(self.indexes) - 1:
            end_page_number = int(self.indexes[index + 1].get_page_number())
        else:
            end_page_number = 'EOF'
        return start_page_number, end_page_number

    def get_index_keys(self):
        return [index.get_key() for index in self.indexes]

    @staticmethod
    def read_index_file(file_directory):
        with open(file_directory, 'r') as file:
            index_list = list()
            for line in file.readlines():
                words = line.split(' ')
                index = Index(words[0], words[1][:-1])
                index_list.append(index)
            return index_list
