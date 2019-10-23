from random import randint, choice
import string
import sys
import operator
import time


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
        self.array = data

    def insertValue(self, element: Data):
        self.array.append(element)

    def removeValue(self, value: int):
        isNotValue = lambda x: x.value is not value
        self.array = filter(isNotValue, self.array)

    def findValue(self, value: int):
        isValue = lambda x: x.value is value
        return filter(isValue, self.array)

    def findValues(self, valueStart: int, valueEnd: int):
        return [element for element in self.array if valueStart <= element.value <= valueEnd]


if __name__ == '__main__':

    user_input_size = 10
    data_set = DataSet(user_input_size)
    # data_set.print_random()
    # data_set.generate_sorted()
    # data_set.print_sorted()

    start = time.time()

    arrayStructure = ArrayStructure(data_set.randomSet)
    arrayStructure.insertValue(Data(100, 'Marcin'))
    arrayStructure.insertValue(Data(110, 'Piotrek'))
    arrayStructure.insertValue(Data(120, 'Maciej'))
    arrayStructure.insertValue(Data(130, 'Bombel'))
    arrayStructure.insertValue(Data(140, 'Koszli'))
    DataSet.print_list(arrayStructure.array)

    DataSet.print_list(arrayStructure.findValue(100))

    DataSet.print_list(arrayStructure.findValues(110, 130))

    arrayStructure.removeValue(100)
    DataSet.print_list(arrayStructure.array)

    end = time.time()
    print(end - start)
