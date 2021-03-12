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

                # Block displacement
                newR = pos[0] + move[0]
                newC = pos[1] + move[1]

                # Is that move possible ?
                possible_move = newR>=0 and newR<state.nbr and newC>=0 and newC<state.nbc and state.grid[newR][newC]==' '

                if(possible_move):

                    new_state = State(copy.deepcopy(state.grid))

                    # Falling while there is free space below it
                    while(newR<state.nbr-1 and state.grid[newR+1][newC]==' '):
                            newR = newR+1

                    #Matching: If after moving/falling the block is at the right position, set grid value to '@'
                    if(state.grid[pos[0]][pos[1]].upper()==goal_state.grid[newR][newC]):
                        new_state.grid[newR][newC] = '@'

                    #Moving: If not a match, simply update structures 
                    else:
                        new_state.grid[newR][newC] = state.grid[pos[0]][pos[1]]
                        new_state.blocks_positions.append((newR,newC))

                    #Erasing last position in any case
                    new_state.grid[pos[0]][pos[1]] = ' '  
                    new_state.blocks_positions.remove(pos) 

                    #Move other blocks consequently: Other blocks may fall due to a block move
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

                    # Check if generated state is not a dead state. If not, had to nodes to expand
                    if not new_state.is_dead():
                        yield (move,new_state)


        

    def goal_test(self, state):
        if all(state.grid[R][C]=='@' for (R,C) in goal_state.blocks_positions):
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
        self.blocks_positions = [] # this extension contains the coordinates of active blocks, once a block has found its target, it is removed from that list
        for i in range(self.nbr):
            for j in range(self.nbc):
                if grid[i][j] not in ['#',' ','@']:
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



    # function is_dead(state): Important function that discards possible dead states
    # Step 1 : List the blocks which are still able to reach at least one of their target (they are "available"), remove others. A block is available if :
    #            - It is not below every possible target.
    #            - There is not a obstacle between him and its target, if on the same line
    # Step 2 : Count the number of goals for each character (ex: 'A'). If available blocks contain enough characters ('a'), then this is not a dead state.

    def is_dead(self):

        # Step 1
        # Blocks are all available by default => remaining
        remaining = copy.deepcopy(self.blocks_positions)

        # For each block, check if it is available. If not, discarded from "remaining"
        for (r,c) in self.blocks_positions:
            available = False

            for (R,C) in goal_state.blocks_positions:
                
                if(self.grid[r][c].upper()==goal_state.grid[R][C]):

                    above = (r<=R)

                    reachable = True
                    if(r==R):
                        left  = min(c,C)+1
                        right = max(c,C)-1
                        for j in range (left,right):
                            if self.grid[r][j] in ['#','@']:
                                reachable = False

                    if(above and reachable):
                        available = True

            if(available==False):
                remaining.remove((r,c))

        # Step 2
        # Count number of goals by character and check is there are enough blocks available in the remaining list
        for (R,C) in goal_state.blocks_positions:  # Counting goals
            val = goal_state.grid[R][C]
            count_goal = 0
            for (R1,C1) in goal_state.blocks_positions:
                if(goal_state.grid[R1][C1]==val and self.grid[R1][C1]!='@'):
                    count_goal += 1
            
            count_avail = 0  
            for (r,c) in remaining:  # Counting available for that character
                if(self.grid[r][c].upper()==val):
                    count_avail += 1

            if count_goal>count_avail: # if not enough available blocks, dead state
                return True

        return False


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

######################
# Heuristic function #
######################
def heuristic(node):
    h = 0.0
    # ...
    # compute an heuristic value
    # ...

    # For the heuristic, we check use three values :
    #        - The sum of all horizontal Manhattan distances between a blocks and their closest target: total_dist
    #        - The sum of distances between each block and their closest edge (where it falls): dist_fall
    #        - An additonal element increased when a block is below any target: below_goal
    total_dist  = 0
    dist_fall   = 0
    for (r,c) in node.state.blocks_positions:
        c_left  = 0
        c_right = 0
        if r+1 != goal_state.nbr:
            for col in range(c,goal_state.nbc):
                if((node.state.grid[r+1][col] in [' ']) or goal_state.grid[r][col]==node.state.grid[r][c].upper()):
                    c_right = col
                    break
            for col in range(0,c):
                if((node.state.grid[r+1][col] in [' ']) or goal_state.grid[r][col]==node.state.grid[r][c].upper()):
                    c_left = col
                    break

        dist_fall += min(c_left,c_right)


        found = False  # is there a goal for the block
        min_dist = (goal_state.nbr+1)+(goal_state.nbc+1)
        for (R,C) in goal_state.blocks_positions:
            if (node.state.grid[r][c].upper() == goal_state.grid[R][C]):
                found = True
                dist = abs(c-C) #+ abs(r-R) # horizontal Manhattan distance
                if dist < min_dist:         # we check the closest target
                    min_dist = dist

        if found:
            total_dist += min_dist

    # Are blocks below a target
    below_goal = 0
    for (r,c) in node.state.blocks_positions:
        for row in range(0,r):
            if(goal_state.grid[row][c] not in ['#','@']):
                below_goal += 1

    # Empirical factors: Overestimation solves faster, but sometimes ignores optimal paths
    h += total_dist*2.5 + dist_fall*1.5 + below_goal

    return h

##############################
# Launch the search in local #
##############################
'''
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
    node, nb_explored, remaining_nodes = astar_graph_search(problem,heuristic)
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
print("* Queue size at goal:\t",  remaining_nodes)
