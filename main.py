from random import randint
import sys
import operator
from timeit import default_timer as timer
from random import sample
from structures import *
import copy
from plotting import *

def generate_random_data_set(size, min_wrapper_size, max_wrapper_size):
    return [Data(randint(0, sys.maxsize), ''.join('A' for _ in range(randint(min_wrapper_size, max_wrapper_size)))) for _ in range(0, size)]


def generate_asc_data_set(size, min_wrapper_size, max_wrapper_size):
    return sorted([Data(randint(0, sys.maxsize), ''.join('A' for _ in range(randint(min_wrapper_size, max_wrapper_size)))) for _ in range(0, size)], key=operator.attrgetter("value"))


def generate_desc_data_set(size, min_wrapper_size, max_wrapper_size):
    return sorted([Data(randint(0, sys.maxsize), ''.join('A' for _ in range(randint(min_wrapper_size, max_wrapper_size)))) for _ in range(0, size)], key=operator.attrgetter("value"), reverse=True)


def generate_data_set(data_set_type, size, min_wrapper_size=1, max_wrapper_size=100):
    func_name = {'asc': 'generate_asc_data_set', 'desc': 'generate_desc_data_set',
                 'random': 'generate_random_data_set'}.get(data_set_type, 'generate_random_data_set')
    return globals()[func_name](size, min_wrapper_size, max_wrapper_size)


def generate_subset(data_set, method, size):
    if method == 'begin':
        return data_set[:size]
    elif method == 'end':
        return data_set[-size:]
    else:
        return get_random_elements(data_set, size)


def insert_elements(structure, data_set):
    start = timer()
    for elem in data_set:
        structure.insert_element(elem)
    end = timer()
    return end - start


def delete_elements(structure, data_set):
    start = timer()
    for elem in data_set:
        structure.remove_element(elem.value)
    end = timer()
    return end - start


def find_elements(structure, data_set):
    start = timer()
    for elem in data_set:
        structure.find_element(elem.value)
    end = timer()
    return end - start


def find_elements_interval(structure, f_min, f_max):
    start = timer()
    structure.find_elements(f_min, f_max)
    end = timer()
    return end - start


def construct(structure, insertion_set, interval):
    timestamps = []
    for inserted in range(0, len(insertion_set), interval):
        start = timer()
        for index in range(interval):
            structure.insert_element(insertion_set[inserted+index])
        end = timer()
        timestamps.append(end-start)
    return timestamps


def get_interval(data_set, percentage):
    data_set = sorted(data_set,  key=operator.attrgetter("value"))
    ln = len(data_set)
    interval_length = int(ln * percentage)
    interval_start = randint(0, ln-1)
    end = interval_start + interval_length
    if end >= ln:
        interval_start = interval_start - (end - ln)-1
        end = end - (end - ln)-1
    return data_set[interval_start].value, data_set[end].value


def get_random_elements(data_set, sample_size):
    return sample(data_set, sample_size)


# def saveResult(file, time):
#     file.write(str(time.insert)+","+str(time.delete)+","+str(time.find)+","+str(time.f_interval)+"\n")


class Result:
    def __init__(self):
        self.array = []
        self.avl = []
        self.bst = []
        self.rb = []


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


def calculate_times(data_set, structure, processing_sets, experiment):
    construct_time = construct(structure, data_set, experiment['construct_interval'])
    find_time = find_elements(structure, processing_sets['find_set'])
    find_interval = find_elements_interval(structure, processing_sets['f_min'], processing_sets['f_max'])
    cpy = copy.deepcopy(structure)
    insert_time = insert_elements(structure, processing_sets['insert_set'])
    delete_time = delete_elements(cpy, processing_sets['delete_set'])
    return [insert_time, delete_time, find_time, find_interval], construct_time


def begin_experiment(experiment):
    toMakeAverage = []
    toMakeAverageConstructTimes = []
    for iteration in range(experiment['iterations']):
        print(iteration)
        result = Result()
        construct_times = Result()
        array_time, avl_time, bst_time, rb_time = [], [], [], []
        for size in range(experiment['min_size'], experiment['max_size']+1, experiment['loop_interval']):
            data_set = generate_data_set(experiment['data_set_gen'], size, experiment['min_wrapper_size'],
                                         experiment['max_wrapper_size'])
            processing_sets = {}
            processing_sets['insert_set'] = generate_data_set(experiment['to_insert']['method'], experiment['to_insert']['size'])
            processing_sets['delete_set'] = generate_subset(data_set, experiment['to_delete']['method'], experiment['to_delete']['size'])
            processing_sets['find_set'] = generate_subset(data_set, experiment['to_find']['method'], experiment['to_find']['size'])
            processing_sets['f_min'], processing_sets['f_max'] = get_interval(data_set, experiment['interval_percentage'])
            if experiment['with_array']:
                res, array_time = calculate_times(data_set, ArrayStructure([]), processing_sets, experiment)
                result.array.append(res)
            res, avl_time = calculate_times(data_set, AVLWrapper(), processing_sets, experiment)
            result.avl.append(res)
            res, bst_time = calculate_times(data_set, BinaryWrapper(), processing_sets, experiment)
            result.bst.append(res)
            res, rb_time = calculate_times(data_set, RBWrapper(), processing_sets, experiment)
            result.rb.append(res)
        if experiment['with_array']:
            construct_times.array.append(array_time)
        construct_times.avl.append(avl_time)
        construct_times.bst.append(bst_time)
        construct_times.rb.append(rb_time)
        toMakeAverage.append(result)
        toMakeAverageConstructTimes.append(construct_times)
    construct_averaged = makeAverage(toMakeAverageConstructTimes)
    result = makeAverage(toMakeAverage)
    if experiment['with_array']:
        plot_all(np.arange(experiment['min_size'], experiment['max_size']+1,  experiment['loop_interval']), result, construct_averaged)
    else:
        plot_tree(np.arange(experiment['min_size'], experiment['max_size']+1,  experiment['loop_interval']), result, construct_averaged)


if __name__ == '__main__':
    experiment1 = {
        'with_array': True,  # True - 4 plots, False - 3 plots
        'min_wrapper_size': 1,
        'max_wrapper_size': 100,
        'data_set_gen': 'random',  # random, asc, desc
        'min_size': 1000,  # min size of the structure
        'max_size': 10000,  # max size of the structure
        'loop_interval': 1000,  # structure size will be incremented by this value. Strarting from min_size until max_size is reached.
        'construct_interval': 1000,  # timestamps frequency while constructing the structure
        'to_insert': {
          'method': 'random',  # should be random
          'size': 100,  # number of elements to insert
        },
        'to_delete': {
            'method': 'random',  # begin - first elements, end - last elements, random - random elements
            'size': 100,  # number of elements to delete
        },
        'to_find': {
            'method': 'random',   # begin - first elements, end - last elements, random - random elements
            'size': 100,  # number of elements to find
        },
        'iterations': 5,
        'interval_percentage': 0.5  # % of elements in interval

    }

    begin_experiment(experiment1)
