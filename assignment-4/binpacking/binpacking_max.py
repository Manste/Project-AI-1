#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>"""
import time

"""Groupe 26"""
from search import *
import sys


class BinPacking(Problem):

    def successor(self, state):
        # swap two items
        for i, bin_i in enumerate(state.bins):
            for j, bin_j in enumerate(state.bins):
                # skip if  it's the same bin is selected
                if i == j:
                    pass
                for item_i, capacity_i in bin_i.items():
                    for item_j, capacity_j in bin_j.items():
                        # if both items have the same capacity, useless swap.
                        # so we skip this, in this case:
                        if capacity_i == capacity_j:
                            pass
                        new_state = State(state.capacity, state.items.copy())
                        new_state.bins = [bin.copy() for bin in state.bins]
                        new_state.bins[i].pop(item_i, None)
                        new_state.bins[j].pop(item_j, None)
                        if new_state.can_fit(new_state.bins[i], capacity_j) and new_state.can_fit(new_state.bins[j], capacity_i):
                            new_state.bins[i][item_j] = capacity_j
                            new_state.bins[j][item_i] = capacity_i
                            yield (item_i, item_j), new_state

        # swap an item and a blank space
        for i, bin_i in enumerate(state.bins):
            bin_capacity = sum(bin_i[el] for el in bin_i)
            miss = state.capacity - bin_capacity
            # skip if there is no misses
            if miss == 0:
                pass
            for j, bin_j in enumerate(state.bins):
                # skip if  it's ourselves
                if i == j:
                    pass
                for item, capacity in bin_j.items():
                    if state.can_fit(state.bins[i], capacity):
                        new_state = State(state.capacity, state.items.copy())
                        new_state.bins = [bin.copy() for bin in state.bins]
                        new_state.bins[j].pop(item, None)
                        new_state.bins[i][item] = capacity
                        if {} in new_state.bins:
                            new_state.bins.remove({})
                        yield tuple(item), new_state

    def fitness(self, state):
        sum_fullness = sum((sum(list(bin_i.values()))/state.capacity)**2 for bin_i in state.bins)/len(state.bins)
        return 1 - sum_fullness

    def value(self, state):
        return self.fitness(state)


class State:

    def __init__(self, capacity, items):
        self.capacity = capacity
        self.items = items
        self.bins = self.build_init()

    # an init state building is provided here but you can change it at will
    def build_init(self):
        init = []
        for ind, size in self.items.items():
            if len(init) == 0 or not self.can_fit(init[-1], size):
                init.append({ind: size})
            else:
                if self.can_fit(init[-1], size):
                    init[-1][ind] = size
        return init

    def can_fit(self, bin, itemsize):
        return sum(list(bin.values())) + itemsize <= self.capacity

    def __str__(self):
        s = ''
        for i in range(len(self.bins)):
            s += ' '.join(list(self.bins[i].keys())) + '\n'
        return s

    def __eq__(self, other):
        return self.bins == other.bins

    def __hash__(self):
        return hash(state.bins)

def read_instance(instanceFile):
    file = open(instanceFile)
    capacitiy = int(file.readline().split(' ')[-1])
    items = {}
    line = file.readline()
    while line:
        items[line.split(' ')[0]] = int(line.split(' ')[1])
        line = file.readline()
    return capacitiy, items

# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current

    for i in range(limit):
        if callback is not None:
            callback(current)
        neighbors = list(current.expand())
        i = 0
        neighbors.sort(key=lambda node: problem.fitness(node.state))
        current = neighbors[0]
        if problem.fitness(current.state) < problem.fitness(best.state):
            best = current
    return best

#####################
#       Launch      #
#####################
if __name__ == '__main__':
    instances_path = "instances/"
    instance_names = ['test', 'i01','i02','i03','i04','i05','i06','i07','i08','i09','i10']

    for instance in [instances_path + name + ".txt" for name in instance_names]:
        info = read_instance(instance)
        init_state = State(info[0], info[1])
        bp_problem = BinPacking(init_state)
        step_limit = 100

        startTime = time.perf_counter()
        node = maxvalue(bp_problem, step_limit)
        endTime = time.perf_counter()

        state = node.state
        print("* Instance:\t", instance)
        print("* Fitness : ", bp_problem.fitness(state))
        print("* NS: ", node.step)
        print("* Execution time:\t", str(endTime - startTime))
        print(state)
    """
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1])
    bp_problem = BinPacking(init_state)
    step_limit = 150
    node = maxvalue(bp_problem, step_limit)
    state = node.state
    print(state)
    """