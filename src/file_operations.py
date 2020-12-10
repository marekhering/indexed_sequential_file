from setup import INDEXES_DIR
from .index import Index


def read_index_file():
    with open(INDEXES_DIR, 'r') as file:
        index_list = list()
        for line in file.readlines():
            words = line.split(' ')
            index = Index(words[0], words[1][:-1])
            index_list.append(index)
        return index_list

