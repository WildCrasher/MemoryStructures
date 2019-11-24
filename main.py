from random import randint, choice
import string
import sys
import operator
from timeit import default_timer as timer
from random import sample
from bintrees import *
import matplotlib.pyplot as plt
import numpy as np


class TimeMeasure:
    def __init__(self):
        self.construct = []
        self.insert = 0
        self.delete = 0
        self.find = 0
        self.f_interval = 0

array_time = TimeMeasure()
avl_time = TimeMeasure()
binary_time = TimeMeasure()
rb_time = TimeMeasure()
construct_interval = 1000  # timestamps frequency while constructing
to_insert = 100  # number of elements to insert
to_delete = 100  # number of elements to delete
find_min = 0  # TODO automatically generate period when given %
find_max = 9000000
iterations = 25


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

    def find_elements(self, start: int, end: int):
        return [element for element in self.data if start <= element.value <= end]


class BinaryWrapper:
    def __init__(self):
        self.root = BinaryTree()

    def insert_element(self, element: Data):
        self.root.insert(element.value, element.text)

    def remove_element(self, value: int):
        self.root.remove(value)

    def find_element(self, value: int):
        return self.root.get_value(value)

    def find_elements(self, start, end):
        return self.root.item_slice(start, end)


class AVLWrapper(BinaryWrapper):
    def __init__(self):
        BinaryWrapper.__init__(self)
        self.root = AVLTree()


class RBWrapper(BinaryWrapper):
    def __init__(self):
        BinaryWrapper.__init__(self)
        self.root = RBTree()

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


def find_elements_interval(structure, f_min, f_max):
    start = timer()
    structure.find_elements(f_min, f_max)
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


def saveResult(file, time):
    file.write(str(time.insert)+","+str(time.delete)+","+str(time.find)+","+str(time.f_interval)+"\n")

def plot_result(x, y, labels, title=""):
    fig = plt.figure()
    ax = plt.subplot(111)
    for i in range(0, len(y)):
        ax.plot(x, y[i], label=labels[i])
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_ylabel('time [s]')
    ax.set_xlabel('number of elements')
    ax.set_title(title)
    intervals = 5
    ax.set_xticks(np.arange(x[0], x[-1]+1, (x[-1]-x[0])/intervals))
    plt.show()


class Result:
    def __init__(self):
        self.array = []
        self.avl = []
        self.bst = []
        self.rb = []

def calculateDataForPlot():
    result = Result()
    for size in range(1000, 10001, 1000):
        data_set = DataSet(size)
        insert_set = DataSet(to_insert).randomSet
        delete_set = get_random_elements(data_set.randomSet, to_delete)

        array_structure = ArrayStructure([])
        array_time.construct = construct(array_structure, data_set.randomSet, construct_interval)
        array_time.insert = insert_elements(array_structure, insert_set)
        array_time.delete = delete_elements(array_structure, delete_set)
        array_time.find = find_elements(array_structure, insert_set)
        array_time.f_interval = find_elements_interval(array_structure, find_min, find_max)

        avl = AVLWrapper()
        avl_time.construct = construct(avl, data_set.randomSet, construct_interval)
        avl_time.insert = insert_elements(avl, insert_set)
        avl_time.delete = delete_elements(avl, delete_set)
        avl_time.find = find_elements(avl, insert_set)
        avl_time.f_interval = find_elements_interval(avl, find_min, find_max)

        binary = BinaryWrapper()
        binary_time.construct = construct(binary, data_set.randomSet, construct_interval)
        binary_time.insert = insert_elements(binary, insert_set)
        binary_time.delete = delete_elements(binary, delete_set)
        binary_time.find = find_elements(binary, insert_set)
        binary_time.f_interval = find_elements_interval(binary, find_min, find_max)

        rbtree = RBWrapper()
        rb_time.construct = construct(rbtree, data_set.randomSet, construct_interval)
        rb_time.insert = insert_elements(rbtree, insert_set)
        rb_time.delete = delete_elements(rbtree, delete_set)
        rb_time.find = find_elements(rbtree, insert_set)
        rb_time.f_interval = find_elements_interval(rbtree, find_min, find_max)

        # for i in range(len(avl_time.construct)):
        #     print(f'{(i+1)*construct_interval} '
        #           f'Array:{array_time.construct[i]} '
        #           f'AVL:{avl_time.construct[i]} '
        #           f'Binary:{binary_time.construct[i]}'
        #           f'RB:{rb_time.construct[i]}'
        #           )
        # print(f'/// Insertion: ///\n'
        #       f'Array: {array_time.insert} AVL: {avl_time.insert} Binary: {binary_time.insert}  RB: {rb_time.insert}\n'
        #       f'/// Deletion: ///\n'
        #       f'Array: {array_time.delete} AVL: {avl_time.delete} Binary: {binary_time.delete} RB: {rb_time.delete}\n'
        #       f'/// Find elements: ///\n'
        #       f'Array: {array_time.find} AVL: {avl_time.find} Binary: {binary_time.find} RB: {rb_time.find}\n'
        #       f'/// Find elements (interval): ///\n'
        #       f'Array: {array_time.f_interval} AVL: {avl_time.f_interval} Binary: {binary_time.f_interval} RB: {rb_time.f_interval}\n'
        #       )
        result.array.append([array_time.insert, array_time.delete, array_time.find, array_time.f_interval])
        result.bst.append([binary_time.insert, binary_time.delete, binary_time.find, binary_time.f_interval])
        result.avl.append([avl_time.insert, avl_time.delete, avl_time.find, avl_time.f_interval])
        result.rb.append([rb_time.insert, rb_time.delete, rb_time.find, rb_time.f_interval])

    return result

def makeAverage(data):
    result = Result()
    array_results = list(map(lambda iteration_result: iteration_result.array, data))
    bst_results = list(map(lambda iteration_result: iteration_result.bst, data))
    avl_results = list(map(lambda iteration_result: iteration_result.avl, data))
    rb_results = list(map(lambda iteration_result: iteration_result.rb, data))

    result.array = np.array(array_results).mean(axis = 0)
    result.bst = np.array(bst_results).mean(axis = 0)
    result.avl = np.array(avl_results).mean(axis = 0)
    result.rb = np.array(rb_results).mean(axis = 0)

    return result

if __name__ == '__main__':
    # file = open("results.csv", "w")
    toMakeAverage = []
    for iteration in range(1, iterations + 1, 1):
        resultDone = calculateDataForPlot()
        toMakeAverage.append(resultDone)

        if iteration == iterations:
            result = makeAverage(toMakeAverage)
            plot_result(np.arange(construct_interval, 10001, construct_interval),
                        [array_time.construct, avl_time.construct, binary_time.construct, rb_time.construct],
                        ["array", "avl", "bst", "red black"], "Construct structure")
            plot_result(np.arange(1000, 10001, 1000), [list(map(lambda x: x[0], result.array)),
                                                       list(map(lambda x: x[0], result.avl)),
                                                       list(map(lambda x: x[0], result.bst)),
                                                       list(map(lambda x: x[0], result.rb))],
                        ["array", "avl", "bst", "red black"], "Insert elements")
            plot_result(np.arange(1000, 10001, 1000), [list(map(lambda x: x[1], result.array)),
                                                       list(map(lambda x: x[1], result.avl)),
                                                       list(map(lambda x: x[1], result.bst)),
                                                       list(map(lambda x: x[1], result.rb))],
                        ["array", "avl", "bst", "red black"], "Delete elements")
            plot_result(np.arange(1000, 10001, 1000), [list(map(lambda x: x[2], result.array)),
                                                       list(map(lambda x: x[2], result.avl)),
                                                       list(map(lambda x: x[2], result.bst)),
                                                       list(map(lambda x: x[2], result.rb))],
                        ["array", "avl", "bst", "red black"], "Find elements")
            plot_result(np.arange(1000, 10001, 1000), [list(map(lambda x: x[3], result.array)),
                                                       list(map(lambda x: x[3], result.avl)),
                                                       list(map(lambda x: x[3], result.bst)),
                                                       list(map(lambda x: x[3], result.rb))],
                        ["array", "avl", "bst", "red black"], "Find elements in interval")
            plot_result(np.arange(1000, 10001, 1000), [list(map(lambda x: x[1], result.avl)),
                                                       list(map(lambda x: x[1], result.bst)),
                                                       list(map(lambda x: x[1], result.rb))],
                        ["avl", "bst", "red black"], "Delete elements")
            plot_result(np.arange(1000, 10001, 1000), [list(map(lambda x: x[2], result.avl)),
                                                       list(map(lambda x: x[2], result.bst)),
                                                       list(map(lambda x: x[2], result.rb))],
                        ["avl", "bst", "red black"], "Find elements")
            plot_result(np.arange(1000, 10001, 1000), [list(map(lambda x: x[3], result.avl)),
                                                       list(map(lambda x: x[3], result.bst)),
                                                       list(map(lambda x: x[3], result.rb))],
                        ["avl", "bst", "red black"], "Find elements in interval")
        # print(f'Array: {len(array_structure.find_elements(find_min, find_max))} '
        #       f'AVL: {len(list(avl.find_elements(find_min, find_max)))} '
        #       f'Binary: {len(list(binary.find_elements(find_min, find_max)))} '
        #       f'RB: {len(list(rbtree.find_elements(find_min, find_max)))}')
    #     file.write(str(size)+"\n")
    #     saveResult(file, array_time)
    #     saveResult(file, avl_time)
    #     saveResult(file, binary_time)
    #     saveResult(file, rb_time)
    # file.close()
