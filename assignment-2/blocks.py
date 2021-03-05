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
        state.blocks, state.check_closed, state.nbFind = state.blocks_positions() # TO REMOVE
        moves = ((0, 1), (-1, 0), (1, 0))

        for block in state.blocks.keys():
            for pos in state.blocks[block]:
                x0, y0 = pos
                actions = [(x0 + x, y0 + y) for x, y in moves]
                valid_actions = self.valid_moves(state, actions)
                successors.extend(self.create_successors(state, valid_actions, block))
                x, y = actions[0]
        return successors

    def valid_moves(self, state, actions):
        return [(x, y)
                 for x, y in actions
                 if state.nbr > x >= 0 and state.nbc > y >= 0 and state.grid[x][y] == ' ']


    def create_successors(self, state, moves, block_id):
        successors = []

        for move in moves:
            if block_id.upper() not in goal_state.blocks.keys():
                return []
            new_state = State(copy.deepcopy(state.grid))

            x, y = new_state.blocks[block_id][0]
            new_state.grid[x][y] = ' '
            new_state.blocks[block_id] = [move]
            x, y = move
            new_state.grid[x][y] = block_id

            a, b = goal_state.blocks[block_id.upper()][0]
            if a == x and b == y:
                new_state.check_closed[block_id][0] = "@"
                new_state.nbFind += 1

            if new_state.nbFind == goal_state.nbFind:
                for block in new_state.check_closed:
                    new_state.check_closed[block] = block.upper()
                    print( new_state.blocks[block])


            new_state.grid[x][y] = new_state.check_closed[block_id][0]
            successors.append((move, new_state))
        return successors



    def goal_test(self, state):
        for block in state.check_closed:
            if any(item.islower() for item in state.check_closed[block]):
                return False
        return True


###############
# State class #
###############
class State:
    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.blocks, self.check_closed, self.nbFind = self.blocks_positions() # List all the blocks positions

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
        nbFind = 0
        for i, lst in enumerate(self.grid):
            for j, el in enumerate(lst):
                if el != "#" and el != " ":
                    if el not in blocks.keys():
                        blocks[el], check_closed[el] = [], []
                    if el.isupper():
                        nbFind += 1
                    blocks[el].append((i, j))
                    check_closed[el].append(el)
        self.update_blocks(blocks)
        return blocks, check_closed, nbFind

    def update_blocks(self, blocks):
        for block in blocks.keys():
            sorted(blocks[block], key=lambda x: -x[1])

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
    tot_h = 0
    for b in blocks.copy():
        if not (b.upper in goal_state.blocks.keys()):
            blocks.pop(b)
            continue

        h = float("inf")
        if distance(blocks[b], goal_state.blocks[b.upper()]) < h:
            h = distance(blocks[b], goal_state.blocks[b.upper()])
        tot_h += h
    return tot_h

##############################
# Launch the search in local #
##############################
#Use this block to test your code in local
# Comment it and uncomment the next one if you want to submit your code on INGInious
instances_path = "instances/instances/"
instance_names = ['a01','a02']

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