# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>'''
import time
import sys
from search import *


#################
# Problem class #
#################
class Knight(Problem):
    """
    fringe.append(Node(problem.initial))
    exploredNodes = 0
    while fringe:
        node = fringe.pop()
        exploredNodes += 1
        if problem.goal_test(node.state):
            return node,exploredNodes, len(fringe)
        fringe.extend(node.expand(problem))
    return None,exploredNodes, len(fringe)
    """

    def __init__(self, state):
        super().__init__(state)
        # List of possible actions available to the agent
        self.actions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

    def successor(self, state):
        possible_states = []
        for action in self.actions:
            curr_i, curr_j = self.get_curr_pos(state)
            row = curr_i + action[0]
            col = curr_j + action[1]

            # Skip if the row in not in the interval [0, nRows[ or
            # the column is not in the interval [0, nCols[
            if row < 0 or col < 0 or row >= state.nRows or col >= state.nCols: continue

            # Check if the position is visited
            if state.grid[row][col] == "\u265E": continue

            # Actions to create a successor
            position = (row, col)
            shape = (state.nRows, state.nCols)
            successor = State(shape, position)
            successor.grid = state.grid.copy()
            successor.grid[curr_i][curr_j] = "\u265E"

            successor.grid[row][col] = "♘"
            print(successor)
            possible_states.append((None, successor))
        return possible_states

    def goal_test(self, state):
        cnt = 0
        for lst in state.grid:
            c = lst.count("\u265E")
            if c < state.nRows - 1:
                return False
            cnt += c
        if cnt == state.nRows * state.nCols - 1:
            return True
        return False

    def get_curr_pos(self, state):
        for i, str in enumerate(state.grid):
            for j, el in enumerate(str):
                if el == "♘":
                    return i, j

###############
# State class #
###############

class State:
    def __init__(self, shape, init_pos):
        self.nRows = shape[0]
        self.nCols = shape[1]
        self.grid = []
        for i in range(self.nRows):
            self.grid.append([" "] * self.nCols)
        self.grid[init_pos[0]][init_pos[1]] = "♘"

    def __str__(self):
        n_sharp = 2 * self.nCols + 1
        s = ("#" * n_sharp) + "\n"
        for i in range(self.nRows):
            s += "#"
            for j in range(self.nCols):
                s = s + str(self.grid[i][j]) + " "
            s = s[:-1]
            s += "#"
            if i < self.nRows - 1:
                s += '\n'
        s += "\n"
        s += "#" * n_sharp
        return s


##############################
# Launch the search in local #
##############################
# Use this block to test your code in local
# Comment it and uncomment the next one if you want to submit your code on INGInious
with open('instances.txt') as f:
    instances = f.read().splitlines()

for instance in instances:
    elts = instance.split(" ")
    shape = (int(elts[0]), int(elts[1]))
    init_pos = (int(elts[2]), int(elts[3]))
    init_state = State(shape, init_pos)

    problem = Knight(init_state)
    # example of bfs tree search
    startTime = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
    endTime = time.perf_counter()

    # example of print
    path = node.path()
    path.reverse()

    print('Number of moves: ' + str(node.depth))
    for n in path:
        print(n.state)  # assuming that the __str__ function of state outputs the correct format
        print()
    print("* Execution time:\t", str(endTime - startTime))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t", remaining_nodes)

####################################
# Launch the search for INGInious  #
####################################
# Use this block to test your code on INGInious
shape = (int(sys.argv[1]), int(sys.argv[2]))
init_pos = (int(sys.argv[3]), int(sys.argv[4]))
init_state = State(shape, init_pos)

problem = Knight(init_state)

# example of bfs tree search
startTime = time.perf_counter()
node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
endTime = time.perf_counter()

# example of print
path = node.path()
path.reverse()

print('Number of moves: ' + str(node.depth))
for n in path:
    print(n.state)  # assuming that the __str__ function of state outputs the correct format
    print()
print("* Execution time:\t", str(endTime - startTime))
print("* Path cost to goal:\t", node.depth, "moves")
print("* #Nodes explored:\t", nb_explored)
print("* Queue size at goal:\t", remaining_nodes)
