# -*-coding: utf-8 -*
'''NAMES OF THE AUTHOR(S): Gaël Aglin <gael.aglin@uclouvain.be>'''
from search import *
import sys
import time
import copy

goal_state = None
#################
# Problem class #
#################
class Blocks(Problem):

    def __init__(self, initial):
        super(Blocks, self).__init__(initial)
        self.possible_moves = ((0, -1), (1, 0), (0, 1))
        self.initial.blocks_positions()

    def successor(self, state):
        successors = []
        state.important = self.pick_down(state)
        for move in state.blocks[state.important[0]].keys():
            x0, y0 = move
            actions = ((x0+x, y0+y) for x, y in self.possible_moves)
            actions = self.valid_moves(state, actions)
            successors += self.create_successors(state, move, actions, state.important[0])
        return successors

    def valid_moves(self, state, actions):
        return ((x, y)
                 for x, y in actions
                 if state.nbr > x >= 0 and state.nbc > y >= 0 and state.grid[x][y] == ' ')


    def create_successors(self, state, old_move, new_moves, block_id):
        successors = []

        for move in new_moves:
            x0, y0 = move
            xd, yd = old_move
            new_state = State(copy.deepcopy(state.grid))
            new_state.blocks = copy.deepcopy(state.blocks)
            new_state.nb_closed = copy.deepcopy(state.nb_closed)
            new_state.grid[xd][yd] = ' '

            if new_state.blocks[block_id][old_move] != '@':
                del new_state.blocks[block_id][old_move]
                new_state.blocks[block_id][move] = block_id

            if state.important[1] == move and goal_state.nb_closed[block_id.upper()] != new_state.nb_closed[block_id]:
                new_state.blocks[block_id][move] = '@'
                new_state.nb_closed[block_id] += 1

            if move in new_state.blocks[block_id].keys():
                new_state.grid[x0][y0] = new_state.blocks[block_id][move]

            #print(new_state)
            #print(state.blocks, '; ', new_state.blocks, '; ', goal_state.blocks)
            successors.append((move, new_state))

        return successors


    def pick_down(self, state):
        x_p, y_p = float("inf"), float("inf")
        for block in goal_state.blocks:
            for x, y in goal_state.blocks[block].keys():
                if x < x_p and (x, y) not in state.blocks[block.lower()].keys():
                    y_p = y
                    x_p = x
                    res = block
        return [res.lower(), (x_p, y_p)]

    def goal_test(self, state):
        for block in goal_state.nb_closed:
            if goal_state.nb_closed[block] != state.nb_closed:
                return False
        return True

###############
# State class #
###############
class State:
    def __init__(self, grid):
        self.nb_closed = {}
        self.blocks = {}
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.blocks_positions()
        self.important = []

    def __str__(self):
        n_sharp = self.nbc + 2
        s = ("#" * n_sharp) + "\n"
        for i in range(self.nbr):
            s += "#"
            for j in range(self.nbc):
                s = s + str(self.grid[i][j])
            s += "#"
            if i < self.nbr - 1:
                s += '\n'
        return s + "\n" + "#" * n_sharp

    # Find all the blocks positions
    def blocks_positions(self):
        for i, lst in enumerate(self.grid):
            for j, el in enumerate(lst):
                if el != "#" and el != " ":
                    if el not in self.nb_closed.keys():
                        self.nb_closed[el] = 0
                        self.blocks[el] = {}
                    if el.isupper():
                        self.nb_closed[(el + '.')[:-1]] += 1
                    self.blocks[(el + '.')[:-1]][(i, j)] = (el + '.')[:-1]

    def __eq__(self, other):
        return self.grid == other.grid

    def __hash__(self):
        return hash(tuple(tuple(lst) for lst in self.grid))


######################
# Auxiliary function #
######################
def readInstanceFile(filename):
    grid_init, grid_goal = map(lambda x: [[c for c in l.rstrip('\n')[1:-1]] for l in open(filename + x)], [".init", ".goalinfo"])
    return grid_init[1:-1], grid_goal[1:-1]


def distance(block1, block2):
    x1, y1 = block1
    x2, y2 = block2
    return abs(x1 - x2) + abs(y1 - y2)

######################
# Heuristic function #
######################
def heuristic(node):
    blocks = node.state.blocks
    main_block = None
    # ...
    # compute an heuristic value
    # ...
    dist = 0
    h = float("inf")

    x_p, y_p = float("inf"), float("inf")
    for block in goal_state.blocks:
        for x, y in goal_state.blocks[block].keys():
            if x < x_p and (x, y) not in node.state.blocks[block.lower()].keys():
                y_p = y
                x_p = x
                main_block = block.lower()

    if main_block is not None:
        for pos1 in blocks[main_block].keys():
            if distance(pos1, (x_p, y_p)) < h:
                h = distance(pos1, (x_p, y_p))
            dist = max(h, dist)
    return dist

##############################
# Launch the search in local #
##############################
#Use this block to test your code in local
# Comment it and uncomment the next one if you want to submit your code on INGInious
instances_path = "instances/instances/"
instance_names = ['a01','a02', 'a03', 'a04', 'a05', 'a07', 'a09'] # to solve: a06, a08, a09

for instance in [instances_path + name for name in instance_names]:
    grid_init, grid_goal = readInstanceFile(instance)
    init_state = State(grid_init)
    goal_state = State(grid_goal)
    problem = Blocks(init_state)

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
    print("* Queue size at goal:\t",  remaining_nodes)


"""
####################################
# Launch the search for INGInious  #
####################################
#Use this block to test your code on INGInious
instance = sys.argv[1]
grid_init, grid_goal = readInstanceFile(instance)
init_state = State(grid_init)
goal_state = State(grid_goal)
problem = Blocks(init_state)

# example of bfs graph search
startTime = time.perf_counter()
node, nb_explored, remaining_nodes = astar_graph_search(problem, heuristic)
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
print("* Queue size at goal:\t",  remaining_nodes)"""