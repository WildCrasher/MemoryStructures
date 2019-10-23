from random import randint, choice
import string
import sys
import operator


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


if __name__ == '__main__':

    user_input_size = 10
    data_set = DataSet(user_input_size)
    data_set.print_random()
    data_set.generate_sorted()
    data_set.print_sorted()
