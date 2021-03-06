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

    def successor(self, state):
        successors = []
        state.blocks, state.nb_closed = state.blocks_positions()
        possible_moves = ((0, 1), (1, 0), (-1, 0))
        for block in state.blocks.keys():
            for move in state.blocks[block].keys():
                x0, y0 = move
                actions = [(x0+x, y0+y) for x, y in possible_moves]
                actions = self.valid_moves(state, actions)
                successors += self.create_successors(state, move, actions, block)
        #print(goal_state.nb_closed)
        return successors

    def valid_moves(self, state, actions):
        return [(x, y)
                 for x, y in actions
                 if state.nbr > x >= 0 and state.nbc > y >= 0 and state.grid[x][y] == ' ']


    def create_successors(self, state, old_move, new_moves, block_id):
        successors = []

        for move in new_moves:
            x0, y0 = move
            xd, yd = old_move
            new_state = State(copy.deepcopy(state.grid))
            new_state.grid[xd][yd] = ' '
            if new_state.blocks[block_id][old_move] != '@':
                del new_state.blocks[block_id][old_move]
                new_state.blocks[block_id][move] = block_id

            if block_id.upper() in goal_state.blocks.keys():
                order_goal_pos = list(goal_state.blocks[block_id.upper()].keys())
                for i in range(0, -len(order_goal_pos), -1):
                    if order_goal_pos[i] in new_state.blocks[block_id].keys():
                        new_state.blocks[block_id][move] = '@'
                        new_state.nb_closed[block_id] += 1

                new_state.grid[x0][y0] = new_state.blocks[block_id][move]

                closed = True
                for block in goal_state.nb_closed:
                    if new_state.nb_closed[block.lower()] != goal_state.nb_closed[block]:
                        closed = False

                if closed:
                    for block in new_state.blocks:
                        for x, y in new_state.blocks[block].keys():
                            new_state.blocks[block][(x, y)] = block.upper()
                            if new_state.grid[x][y] == '@':
                                new_state.grid[x][y] = block.upper()
                            else:
                                new_state.grid[x][y] = ' '

                successors.append((move, new_state))

        return successors

    def goal_test(self, state):
        return state.grid == goal_state.grid

###############
# State class #
###############
class State:
    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.blocks, self.nb_closed = self.blocks_positions()

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
        blocks = {}
        check_closed = {}
        for i, lst in enumerate(self.grid):
            for j, el in enumerate(lst):
                if el != "#" and el != " ":
                    if el not in check_closed.keys():
                        check_closed[el] = 0
                        blocks[el] = {}
                    if el.isupper():
                        check_closed[el] += 1
                    blocks[el][(i, j)] = el
        self.update_blocks(blocks)
        return blocks, check_closed

    def update_blocks(self, blocks):
        for b in blocks:
            sorted(blocks[b].items(), key=lambda item: item[0][1])

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
    # ...
    # compute an heuristic value
    # ...
    dist = 0
    for block in blocks:
        if block.upper() in goal_state.nb_closed.keys():
            h = float("inf")
            for pos1 in blocks[block].keys():
                for pos2 in goal_state.blocks[block.upper()].keys():
                    if distance(pos1, pos2) < h:
                        h = distance(pos1, pos2)
            dist = max(dist, h)
    return dist

##############################
# Launch the search in local #
##############################
#Use this block to test your code in local
# Comment it and uncomment the next one if you want to submit your code on INGInious
instances_path = "instances/instances/"
instance_names = ['a01','a02', 'a03']

for instance in [instances_path + name for name in instance_names]:
    grid_init, grid_goal = readInstanceFile(instance)
    init_state = State(grid_init)
    goal_state = State(grid_goal)
    problem = Blocks(init_state)

    # example of bfs tree search
    startTime = time.perf_counter()
    node, nb_explored, remaining_nodes = best_first_graph_search(problem, heuristic)
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