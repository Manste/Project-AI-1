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
        for pos in state.blocks_positions: 
            for move in ((0,1),(0,-1)):

                newR = pos[0] + move[0]
                newC = pos[1] + move[1]

                possible_move = newR>=0 and newR<state.nbr and newC>=0 and newC<state.nbc and state.grid[newR][newC]==' '


                if(possible_move):

                    new_state = State(copy.deepcopy(state.grid))

                    # Falling
                    while(newR<state.nbr-1 and state.grid[newR+1][newC]==' '):
                            newR = newR+1

                    #Matching
                    if(state.grid[pos[0]][pos[1]].upper()==goal_state.grid[newR][newC]):
                        new_state.grid[newR][newC] = '@'

                    #Moving    
                    else:
                        new_state.grid[newR][newC] = state.grid[pos[0]][pos[1]]
                        new_state.blocks_positions.append((newR,newC))

                    #Erasing last position in any case
                    new_state.grid[pos[0]][pos[1]] = ' '  
                    new_state.blocks_positions.remove(pos)

                    #Move other blocks consequently
                    moving=True
                    while moving:
                        moving=False
                        for block in new_state.blocks_positions:
                            row = block[0]
                            col = block[1]
                            if(row<new_state.nbr-1 and new_state.grid[row+1][col]==' '):
                                moving=True                            
                                while(row<new_state.nbr-1 and new_state.grid[row+1][col]==' '):
                                   row=row+1
                                new_state.grid[row][col] = new_state.grid[block[0]][block[1]]
                                new_state.grid[block[0]][block[1]] = ' '
                                new_state.blocks_positions.remove(block)
                                new_state.blocks_positions.append((row,col))

                    if not new_state.is_dead():
                        #print(new_state)
                        yield (move,new_state)


        

    def goal_test(self, state):
        blocks_tofind = len(goal_state.blocks_positions)
        blocks_found  = 0
        for i in range(state.nbr):
            for j in range(state.nbc):
                if state.grid[i][j]=='@':
                    blocks_found = blocks_found+1
        if blocks_found==blocks_tofind:
            return True
        
        return False


###############
# State class #
###############
class State:
    def __init__(self, grid):
        self.nbr = len(grid)
        self.nbc = len(grid[0])
        self.grid = grid
        self.blocks_positions = []
        for i in range(self.nbr):
            for j in range(self.nbc):
                if grid[i][j] not in ['#',' ']:
                    self.blocks_positions.append((i,j))

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

    def is_dead(self):

        dead_blocks = []

        # Test all blocks: If at least one of them is in dead state, then the entire state is a deadlock
        for (r,c) in self.blocks_positions:
            goals = []
            val   = self.grid[r][c]
            for (R,C) in goal_state.blocks_positions:
                if(goal_state.grid[R][C]==val.upper()):
                    goals.append((R,C))
            
            # If no goal for that block, that block is not to be casted
            if len(goals)==0:
                #print("size0",val,dead_blocks)
                dead_blocks.append(False)
            else:
                # Block has at least one empty spot available BELOW its current position
                res = True
                for (R,C) in goals:
                    if R>=r:
                        res=False
                        break
                dead_blocks.append(res)

        if all(state==False for state in dead_blocks):
            return False
        else:
            return True


            

    def __eq__(self, other):
        return self.grid == other.grid

    def __hash__(self):
        return hash(tuple(tuple(lst) for lst in self.grid))
        #return has(str(self))


######################
# Auxiliary function #
######################
def readInstanceFile(filename):
    grid_init, grid_goal = map(lambda x: [[c for c in l.rstrip('\n')[1:-1]] for l in open(filename + x)], [".init", ".goalinfo"])
    return grid_init[1:-1], grid_goal[1:-1]

######################
# Heuristic function #
######################
def heuristic(node):
    h = 0.0
    # ...
    # compute an heuristic value
    # ...
    # Compute sum of Manhattan distances between blocks and their closest objective


    for (r,c) in node.state.blocks_positions:
        min_dist = (goal_state.nbr+1)+(goal_state.nbc+1) # max
        found = False  # is there a goal for the block
        for (R,C) in goal_state.blocks_positions:
            if (node.state.grid[r][c].upper() == goal_state.grid[R][C]):
                found = True
                dist = abs(r-R) + abs(c-C) # Manhattan
                if dist < min_dist:
                    min_dist = dist
        if found:
            h = h + min_dist   


    return h

##############################
# Launch the search in local #
##############################
#Use this block to test your code in local
# Comment it and uncomment the next one if you want to submit your code on INGInious
instances_path = "instances/"
instance_names = ['a10']
#instance_names = ['a01','a02','a03','a04','a05','a06','a07','a08','a09','a10','a11']

for instance in [instances_path + name for name in instance_names]:
    print(instance)
    grid_init, grid_goal = readInstanceFile(instance)
    init_state = State(grid_init)
    goal_state = State(grid_goal)

    problem = Blocks(init_state)

    # example of bfs tree search
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
    print("* Queue size at goal:\t",  remaining_nodes)



####################################
# Launch the search for INGInious  #
####################################
'''
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
print("* Queue size at goal:\t",  remaining_nodes)
'''