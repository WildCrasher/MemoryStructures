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

    def insert_element(self, element: Data):
        self.data.append(element)

    def remove_element(self, value: int):
        self.data = list(filter(lambda x: x.value is not value, self.data))

    def find_element(self, value: int):
        return list(filter(lambda x: x.value is value, self.data))

    def find_elements(self, valueStart: int, valueEnd: int):
        return [element for element in self.data if valueStart <= element.value <= valueEnd]


class AVLWrapper:
    def __init__(self):
        self.root = AVLTree()

    def insert_element(self, element: Data):
        self.root.insert(element.value, element.text)

    def remove_element(self, value: int):
        self.root.remove(value)

    def find_element(self, value: int):
        return self.root.get_value(value)


class TimeMeasure:
    def __init__(self):
        self.construct = []
        self.insert = 0
        self.delete = 0
        self.find = 0


def insert_elements(structure, elements):
    start = timer()
    for elem in elements:
        structure.insert_element(elem)
    end = timer()
    return end - start


def delete_elements(structure, elements):
    start = timer()
    for elem in elements:
        structure.remove_element(elem.value)
    end = timer()
    return end - start


def find_elements(structure, elements):
    start = timer()
    for elem in elements:
        structure.find_element(elem.value)
    end = timer()
    return end - start


def get_random_elements(dataset, sample_size):
    return sample(dataset, sample_size)


def construct(structure, insertion_set, interval):
    inserted = 0
    timestamps = []
    while inserted < len(insertion_set):
        start = timer()
        for index in range(interval):
            structure.insert_element(insertion_set[inserted+index])
        end = timer()
        timestamps.append(end-start)
        inserted += interval
    return timestamps


if __name__ == '__main__':
    size = 10000  # number of elements in a structure
    construct_interval = 100  # timestamps frequency while constructing
    to_insert = 100  # number of elements to insert
    to_delete = 100  # number of elements to delete

    array_time = TimeMeasure()
    avl_time = TimeMeasure()

    data_set = DataSet(size)
    insert_set = DataSet(to_insert).randomSet
    delete_set = get_random_elements(data_set.randomSet, to_delete)

    array_structure = ArrayStructure([])
    array_time.construct = construct(array_structure, data_set.randomSet, construct_interval)
    array_time.insert = insert_elements(array_structure, insert_set)
    array_time.delete = delete_elements(array_structure, delete_set)
    array_time.find = find_elements(array_structure, insert_set)

    avl = AVLWrapper()
    avl_time.construct = construct(avl, data_set.randomSet, construct_interval)
    avl_time.insert = insert_elements(avl, insert_set)
    avl_time.delete = delete_elements(avl, delete_set)
    avl_time.find = find_elements(avl, insert_set)

    for i in range(len(avl_time.construct)):
        print(f'{(i+1)*construct_interval} Array:{array_time.construct[i]} AVL:{avl_time.construct[i]}')
    print(f'/// Insertion: ///\n'
          f'Array: {array_time.insert} AVL: {avl_time.insert} \n'
          f'/// Deletion: ///\n'
          f'Array: {array_time.delete} AVL: {avl_time.delete} \n'
          f'/// Find elements: ///\n'
          f'Array: {array_time.find} AVL: {avl_time.find} \n'
          )
