from random import randint, choice
import string
import sys
import operator
from timeit import default_timer as timer
from random import sample
from bintrees import *


class Data:
    def __init__(self, value, text):
        self.value = value
        self.text = text


class DataSet:
    def __init__(self, size=0):
        self.size = size
        self.randomSet = []
        self.sortedSet = []
        self.generate_random()

    def generate_random(self):
        for _ in range(0, self.size):
            self.randomSet.append(Data(randint(0, sys.maxsize),
                                       ''.join(choice(string.ascii_lowercase) for _ in range(randint(1, 100)))))

    def generate_sorted(self):
        self.sortedSet = sorted(self.randomSet, key=operator.attrgetter("value"))

    def print_random(self):
        self.print_list(self.randomSet)

    def print_sorted(self):
        self.print_list(self.sortedSet)

    @staticmethod
    def print_list(list_to_print):
        print(f'//////////////')
        for i in list_to_print:
            print(f'{i.value} {i.text}.')


class ArrayStructure:
    def __init__(self, data):
        self.data = data

    def insert_value(self, element: Data):
        self.data.append(element)

    def remove_value(self, value: int):
        isNotValue = lambda x: x.value is not value
        self.data = list(filter(isNotValue, self.data))

    def find_value(self, value: int):
        isValue = lambda x: x.value is value
        return list(filter(isValue, self.data))

    def find_values(self, valueStart: int, valueEnd: int):
        return [element for element in self.data if valueStart <= element.value <= valueEnd]


class TimeMeasure:
    def __init__(self):
        self.insert = 0
        self.delete = 0
        self.search = 0
        self.insert_avl = 0
        self.delete_avl = 0
        self.search_avl = 0



def insert_elements(structure, elements):
    start = timer()
    for elem in elements:
        structure.insert_value(elem)
    end = timer()
    return end - start


def delete_elements(structure, elements):
    start = timer()
    for elem in elements:
        structure.remove_value(elem.value)
    end = timer()
    return end - start


def find_elements(structure, elements):
    start = timer()
    for elem in elements:
        structure.find_value(elem.value)
    end = timer()
    return end - start


def get_random_elements(dataset, sample_size):
    return sample(dataset, sample_size)


def insert_elements_AVL(structure, elements):
    start = timer()
    for elem in elements:
        structure.insert(elem.value, elem.text)
    end = timer()
    return end - start

def delete_elements_AVL(structure, elements):
    start = timer()
    for elem in elements:
        structure.remove(elem.value)
    end = timer()
    return end - start


if __name__ == '__main__':

    user_input_size = 10
    insert_items_size = 20
    delete_items_size = 5
    search_items_size = 10
    data_set = DataSet(user_input_size)
    insert_set = DataSet(insert_items_size).randomSet
    delete_set = get_random_elements(data_set.randomSet, delete_items_size)
    array_time = TimeMeasure()
    array_structure = ArrayStructure(data_set.randomSet)
    array_time.insert = insert_elements(array_structure, insert_set)
    array_time.delete = delete_elements(array_structure, delete_set)
    search_set = get_random_elements(array_structure.data, search_items_size)
    array_time.search = find_elements(array_structure, search_set)

    root = AVLTree()
    array_time.insert_avl = insert_elements_AVL(root, insert_set)
    array_time.delete_avl = delete_elements_AVL(root, delete_set) #cos z kluczami chyba nie tak

    # DataSet.print_list(array_structure.find_values(110, 130))
    print(f'Array insertion time: {array_time.insert} \n'
          f'Array deletion time: {array_time.delete}. \n'
          f'Array search time: {array_time.search}. \n'
          f'AVL insertion time: {array_time.insert_avl}. \n'
          f'AVL deletion time: {array_time.delete_avl}. \n')

