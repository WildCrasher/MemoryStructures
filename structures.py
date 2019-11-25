from bintrees import *


class Data:
    def __init__(self, value, text):
        self.value = value
        self.text = text


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

