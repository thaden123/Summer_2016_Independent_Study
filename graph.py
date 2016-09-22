import time
import random


class Node:
    # All initialized nodes have a name, and adjacency list
    def __init__(self, name):
        self.name = name
        self.list = []

    # Adds an adjacent Neighbor
    def add_neighbor(self, neighbor):
        self.list.append(neighbor)

    # Returns the name of the node, used when instance is passed instead of index
    def get_name(self):
        return self.name

    # Returns if neighbor is a Neighbor
    def points_to(self, neighbor):
        return neighbor in self.list

    # Sorts list of Neighbors for optimization, called by Graph.sort
    def sort(self):
        self.list.sort()
        self.list.append(None)


class Graph:
    # Initializes normal and transpose adjacency lists
    def __init__(self, a):
        self.list = [None] * a
        self.transpose = [None] * a

    # Adds a node only if it has not been initialized
    def add_node(self, a):
        if self.list[int(a)] is None:
            self.list[int(a)] = Node(a)
            self.transpose[int(a)] = Node(a)

    # Adds both normal and transpose edges
    def add_edge(self, a, b):
        self.add_node(a)
        self.add_node(b)
        self.list[int(a)].add_neighbor(b)
        self.transpose[int(b)].add_neighbor(a)

    # Sorts each individual adjacency list to optimize performance
    def sort(self):
        for x in range(len(self.list)):
            if not self.list[x] is None:
                self.list[x].sort()
                self.transpose[x].sort()

    # Selects two random nodes
    def sample(self, l):
        a = []
        b = []
        t = []
        while len(a) < l:
            x = random.sample(self.list, 2)
            if x[0] is not None and x[1] is not None:
                a.append(x[0])
                b.append(x[1])
                t.append(self.transpose[self.list.index(x[1])])
        return a, b, t

    # custom print function for list of nodes
    @staticmethod
    def print_nodes(a):
        b = []
        for x in a:
            b.append(x.get_name())
        print b

    # custom time function
    @staticmethod
    def sugar_time(x):
        if x is 1:
            return "1 second"
        if x < 60:
            return str(x) + " seconds"
        if x is 60:
            return "1 minute"
        if x < 3600:
            return str(x / 60) + " minutes"
        if x is 3600:
            return "1 hour"
        if x < 86400:
            return str(x / 3600) + " hours"
        if x is 86400:
            return "1 day"
        if x < 31536000:
            return str(x / 86400) + " days"
        if x is 31536000:
            return "1 year"
        return str(x / 31536000) + " years"

    # One Sided Breadth-first Search Algorithm
    def one_sided(self, a, b):
        START_TIME = time.time()
        list_A = [a.get_name()]
        queue_A = [a]
        # Traceback used to double check whether there is a path from A to B on success
        traceback_list = [None]
        # External loop iterates through queue_A
        while len(queue_A) != 0:
            current_node = queue_A[0]
            del queue_A[0]
            count = int(0)
            current_neighbor = current_node.list[count]
            # Internal loop iterates through all nodes adjacent to current_node
            while current_neighbor is not None:
                if current_neighbor not in list_A:
                    list_A.append(current_neighbor)
                    traceback_list.append(current_node.get_name())
                    queue_A.append(self.list[int(current_neighbor)])
                    if b.get_name() == current_neighbor:
                        # Success, proceeds to test path and length
                        testing_list = [self.list[int(list_A[-1])]]
                        current_traceback = traceback_list[-1]
                        while current_traceback is not None:
                            testing_list.append(self.list[int(current_traceback)])
                            current_traceback = traceback_list[list_A.index(current_traceback)]
                        return time.time() - START_TIME, True, len(testing_list), testing_list
                count += 1
                current_neighbor = current_node.list[count]
        # Failure
        return time.time() - START_TIME, False, 0, []

    # Traditional two sided breadth first search
    def two_sided(self, a, b):
        START_TIME = time.time()
        list_A = [a.get_name()]
        list_B = [b.get_name()]
        queue_A = [a]
        queue_B = [b]
        # Tracebacks used to double check whether there is a path from A to B on success
        traceback_list_A = [None]
        traceback_list_B = [None]
        toggle = 'N'
        pivotA = int(1)
        pivotB = int(1)
        while len(queue_A) != 0 and len(queue_B) != 0:
            # first side iteration
            for i in range(pivotA):
                current = queue_A[0]
                del queue_A[0]
                cou = int(0)
                current_neighbor = current.list[cou]
                while current_neighbor is not None:
                    if current_neighbor not in list_A:
                        list_A.append(current_neighbor)
                        traceback_list_A.append(current.get_name())
                        queue_A.append(self.list[current_neighbor])
                        if current_neighbor in list_B:
                            last = current_neighbor
                            current_traceback = traceback_list_B[list_B.index(last)]
                            while current_traceback is not None:
                                list_A.append(current_traceback)
                                traceback_list_A.append(last)
                                last = current_traceback
                                current_traceback = traceback_list_B[list_B.index(last)]
                            testing_list = [self.list[int(list_A[-1])]]
                            current_traceback = traceback_list_A[-1]
                            while current_traceback is not None:
                                testing_list.append(self.list[int(current_traceback)])
                                current_traceback = traceback_list_A[list_A.index(current_traceback)]
                            return time.time() - START_TIME, True, (len(testing_list)), testing_list
                    cou += 1
                    current_neighbor = current.list[cou]
            pivotA = len(queue_A)
            # second side iteration
            for i in range(pivotB):
                current = queue_B[0]
                del queue_B[0]
                cou = int(0)
                current_neighbor = current.list[cou]
                while current_neighbor is not None:
                    if current_neighbor not in list_B:
                        list_B.append(current_neighbor)
                        traceback_list_B.append(current.get_name())
                        queue_B.append(self.transpose[current_neighbor])
                        if current_neighbor in list_A:
                            last = current_neighbor
                            current_traceback = traceback_list_A[list_A.index(last)]
                            while current_traceback is not None:
                                list_B.append(current_traceback)
                                traceback_list_B.append(last)
                                last = current_traceback
                                current_traceback = traceback_list_A[list_A.index(last)]
                            testing_list = [self.list[int(list_B[-1])]]
                            current_traceback = traceback_list_B[-1]
                            while current_traceback is not None:
                                testing_list.append(self.list[int(current_traceback)])
                                current_traceback = traceback_list_B[list_B.index(current_traceback)]
                            return time.time() - START_TIME, True, (len(testing_list)), testing_list
                    cou += 1
                    current_neighbor = current.list[cou]
            pivotB = len(queue_B)
        # Failure
        return time.time() - START_TIME, False, 0, []
