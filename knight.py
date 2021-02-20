# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>'''
import time
import sys
from search import *
import copy


#################
# Problem class #
#################
class Knight(Problem):
    # List of possible actions available to the agent
    actions = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))

    def successor(self, state):
        sucessors = self.get_successors(state)
        minimums = []
        if len(sucessors) == 0: return minimums
        min = sucessors[0]
        for s in sucessors:
            if len(self.get_successors(s[1])) <= len(self.get_successors(min[1])):
                min = s
                minimums.append(s)
        return minimums[-2:][::-1]

    def goal_test(self, state):
        for lst in state.grid:
            if any(" " in s for s in lst):
                return False
        return True

    def get_successors(self, state):
        next_states = []
        pos_x, pos_y = state.position
        positions = set((pos_x + x, pos_y + y) for x, y in self.actions)
        positions = set((x, y) for x, y in positions
                         if 0 <= x < state.nRows and 0 <= y < state.nCols # Skip if the row in not in the interval
                                                                          # [0, nRows[ or the column is not in the interval [0, nCols[
                         and not state.grid[x][y] == "\u265E" # Check if the position is visited
                    )
        for pos in positions:
            successor = State((state.nRows, state.nCols),  (pos[0], pos[1]))
            successor.grid = copy.deepcopy(state.grid)
            successor.grid[pos_x][pos_y] = "\u265E"
            successor.grid[pos[0]][pos[1]] = "♘"

            next_states.append((pos, successor))
        return next_states


###############
# State class #
###############

class State:
    def __init__(self, shape, init_pos):
        self.nRows = shape[0]
        self.nCols = shape[1]
        self.grid = []
        self.position = init_pos
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

    def __eq__(self, other):
        if (self.nRows != other.nRows) or (self.nCols != other.nCols) or (self.position[0] != other.position[0]) or (self.position[1] != other.position[1]):
            return False
        for i in range(self.nRows):
            for j in range(self.nCols):
                if self.grid[i][j] != other.grid[i][j]:
                    return False
        return True

    def __hash__(self):
        cnt = 0
        for i in range(self.nRows):
            for j in range(self.nCols):
                cnt += hash(self.grid[i][j])
        return cnt


def breadth_first_graph_search(problem):
    fringe = FIFOQueue()
    closed = {}
    fringe.append(Node(problem.initial))
    exploredNodes = 0
    while fringe:
        node = fringe.pop()
        exploredNodes += 1
        print(len(fringe))
        if problem.goal_test(node.state):
            return node,exploredNodes, len(fringe)
        if node.state not in closed:
            closed[node.state] = True
            fringe.extend(node.expand(problem, closed))
            print(len(fringe))
    return None,exploredNodes, len(fringe)


##############################
# Launch the search in local #
##############################
# Use this block to test your code in local
# Comment it and uncomment the next one if you want to submit your code on INGInious
with open('instances.txt') as f:
    instances = f.read().splitlines()
cnt = 0
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

    if node is None:
        cnt += 1
        print("\n\n\n####ECHEC " + str(cnt) + "\n\n\n",)
        continue

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
node, nb_explored, remaining_nodes = depth_first_graph_search(problem)
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

