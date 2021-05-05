#! /usr/bin/env python3
"""NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>"""
from search import *
import sys
import copy
import time


class BinPacking(Problem):

    def successor(self, state):

        for bin in range(len(state.bins)): # indices !

            other_bins = [i for i in range(len(state.bins))] # indices !
            other_bins.pop(bin)

            for key_bin, val_bin in state.bins[bin].items():
                for ob in other_bins:

                    new_state_move = copy.deepcopy(state)
                    new_state_move.move(bin, key_bin, ob)
                    yield ( None, new_state_move)

                    for key_other, val_other in state.bins[ob].items():
                        new_state_exchange = copy.deepcopy(state)
                        new_state_exchange.exchange(bin, key_bin, ob, key_other)
                        yield( None, new_state_exchange)



    def fitness(self, state):
        """
        :param state:
        :return: fitness value of the state in parameter
        """
        C = state.capacity
        k = len(state.bins)
        s = 0
        for b in state.bins:
            fullness = 0
            for v in b.values():
                fullness += v
            s += (fullness/C)**2   
        return 1 - s/k

    


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


    # exchanges element key1 in bin1 with element key2 in bin2, if bins capacities allow it
    def exchange(self, bin1, key1, bin2, key2):

        if bin1==bin2:
            pass

        key1 = str(key1)
        key2 = str(key2)
        val1 = self.bins[bin1][key1]
        val2 = self.bins[bin2][key2]

        self.bins[bin1].pop(key1)
        self.bins[bin2].pop(key2)

        if self.can_fit(self.bins[bin1], val2) and self.can_fit(self.bins[bin2], val1):
            self.bins[bin1][key2] = val2
            self.bins[bin2][key1] = val1
        else:
            self.bins[bin1][key1] = val1
            self.bins[bin2][key2] = val2

    # moves element key1 from bin1 to bin2 
    def move(self, bin1, key1, bin2):
        
        if bin1==bin2:
            pass

        key1 = str(key1)
        val1 = self.bins[bin1][key1]

        if self.can_fit(self.bins[bin2], val1):
            self.bins[bin1].pop(key1)
            self.bins[bin2][key1] = val1
            if len(self.bins[bin1])==0:
                self.bins.pop(bin1)



    def __str__(self):
        s = ''
        for i in range(len(self.bins)):
            s += ' '.join(list(self.bins[i].keys())) + '\n'
        return s


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

    current = LSNode(problem, problem.initial, 0)
    best = current

    for i in range(limit):
        neighbors = list(current.expand())
        neighbors.sort(key=lambda node: problem.fitness(node.state))
        current = neighbors[0]
        if problem.fitness(current.state) < problem.fitness(best.state):
            best = LSNode(problem, current.state, i+1)
    return best


# Attention : Depending of the objective function you use, your goal can be to maximize or to minimize it
def randomized_maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current

    for i in range(limit):
        neighbors = list(current.expand())
        neighbors.sort(key=lambda node: problem.fitness(node.state))
        current = neighbors[random.randint(0, 4)]
        if problem.fitness(current.state) < problem.fitness(best.state):
            best = LSNode(problem, current.state, i + 1)
    return best


#####################
#       Launch      #
#####################
if __name__ == '__main__':
    instances_path = "instances/"
    instance_names = ['i01','i02','i03','i04','i05','i06','i07','i08','i09','i10']

    for instance in [instances_path + name + ".txt" for name in instance_names]:
        info = read_instance(instance)
        init_state = State(info[0], info[1])
        bp_problem = BinPacking(init_state)
        step_limit = 100

        startTime = time.perf_counter()
        node = randomized_maxvalue(bp_problem, step_limit)
        endTime = time.perf_counter()

        state = node.state
        print("* Instance:\t", instance)
        print("* Execution time:\t", str(endTime - startTime))
        print(state)

"""
    info = read_instance(sys.argv[1])
    init_state = State(info[0], info[1])
    bp_problem = BinPacking(init_state)
    step_limit = 100
    node = randomized_maxvalue(bp_problem, step_limit)
    state = node.state
    print(state)"""
