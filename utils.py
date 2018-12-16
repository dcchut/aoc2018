import multiprocessing
import re

from joblib import Parallel, delayed


def load_input(filename):
    # load the input data
    with open(filename, 'r') as fh:
        data = fh.read()

    return data.split('\n')


def get_numbers(string):
    # get all of the numbers appearing in a given string
    return mapint(re.findall(r"(-?\d+)", string))


def mapint(li):
    return [int(q) for q in li]


def parallel_map(inputs, fn, unpack=False):
    num_cores = multiprocessing.cpu_count()

    # if the unpack parameter is true, then unpack each input into our function
    if unpack:
        return Parallel(n_jobs=num_cores)(delayed(fn)(*q) for q in inputs)
    else:
        return Parallel(n_jobs=num_cores)(delayed(fn)(q) for q in inputs)


class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


# A basic circular doubly linked list implementation
class CircularDoublyLinkedList:
    def __init__(self):
        self.first = None

    # insert new_node <after> node
    def insert(self, node, new_node):
        new_node.prev = node
        new_node.next = node.next
        new_node.next.prev = new_node
        node.next = new_node

    # insert new_node at end
    def append(self, new_node):
        # if the list is empty, then this is our list!
        if self.first is None:
            self.first = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            # otherwise insert after the last thing in our list
            self.insert(self.first.prev, new_node)

    # remove a node from the list
    def remove(self, node):
        # if the list has a single element
        if self.first.next == self.first:
            self.first = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            # update self.first if we removed the first node
            if self.first == node:
                self.first = node.next