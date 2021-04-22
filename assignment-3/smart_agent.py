
from core.player import Player
from core import Color
from seega.seega_rules import SeegaRules
from copy import deepcopy


DEBUG = False
def log(message):
    if DEBUG:
        print(message)


class AI(Player):

    in_hand = 12
    score = 0
    name = "Template"

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value
        self.opponentColor = Color(-color.value)
        self.boring_states = []

        print("Position (=color.value):"+ str(self.position))
        print("My color: "+str(self.color))
        print("Opponent color: "+str(self.opponentColor))

    def play(self, state, remain_time):
        print("")
        print(f"Player {self.position} is playing.")
        print("time remain is ", remain_time, " seconds")
        log("Latest player: " + str(state.get_latest_player()))
        log("Next   player: " + str(state.get_next_player())) # current
        log("Boring moves: "+str(state.boring_moves)+"/"+str(state.just_stop))
        log("Boring states detected: "+str(self.boring_states))
        return minimax_search(state, self)


    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """

    def sort_successors(self, entry):
        return entry[1] # evaluation

    def successors(self, state):
        actions = SeegaRules.get_player_actions(state, state.get_next_player())
        successors_evaluations  = []
        log("Successors evaluation:")
        for act in actions:
            new_state = deepcopy(state)
            if SeegaRules.act(new_state, act, state.get_next_player()):
                successor  = (act, new_state)
                evaluation = self.evaluate(successor[1]) # evaluate successor state
                successors_evaluations.append((successor, evaluation))
                """
                if not new_state.captured and new_state.phase==2:
                    if not self.inBoardList(new_state.get_board(), self.boring_states):
                        #print("Boring states detected: "+str(self.boring_states))
                        self.boring_states.append(new_state.get_board())

                        successors_evaluations.append((successor, evaluation))
                    else:
                        print("Boring state discarded:")
                        print(successor[0].action)

                else:
                    successors_evaluations.append((successor, evaluation))
                """


        if(state.get_next_player()==self.position): # max = descending order
            successors_evaluations.sort(key=self.sort_successors, reverse=True)
        else: # min = ascending order
            successors_evaluations.sort(key=self.sort_successors, reverse=False)

        successors = []
        for s in successors_evaluations:
            successors.append(s[0])

        log(str(len(successors)) +" successors found")
        for i,s in enumerate(successors_evaluations):
            log(str(i) + ".   action: " + str(s[0][0].action) + "    value = " + str(s[1]))
        log("==========================================================")
        log("")

        return successors
    
    """
    Boring states storage
    """

    def sameBoard(self, board1, board2):
        x1 = board1.board_shape[0]
        x2 = board2.board_shape[0]
        y1 = board1.board_shape[1]
        y2 = board2.board_shape[1]
        if x1==x2 and y1==y2:
            for x in range(x1):
                for y in range(x2):
                    if not board1.get_cell_color((x,y))==board2.get_cell_color((x,y)):
                        return False
            return True
        else:
            return False

    def inBoardList(self, board, boardList):
        for b in boardList:
            if self.sameBoard(b, board):
                return True
        return False


    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):

        if state.phase==1:
            if depth>0:
                return True
            else:
                return False

        toVisit = []
        cache   = []

        toVisit.append(state)

        
        while toVisit:
            detectedBoring = False
            current_state = toVisit.pop()

            print("cache length "+str(len(cache)))
            for c in cache:
                board1 = c.get_board()
                board2 = current_state.get_board()
                if self.sameBoard(board1, board2):
                    detectedBoring = True
                    break
            
            if detectedBoring:
                print("detected boring")
                continue

            if len(cache)==50:
                cache.pop()
            cache.append(current_state)

            successors = self.successors(current_state)
            for s in successors:
                toVisit.append(s[1])  # depth first search

            if SeegaRules.is_end_game(current_state):
                latest_player_score = state.score[current_state.get_latest_player()]
                print(state.score)
                if latest_player_score >= current_state.MAX_SCORE:
                    return False # dont cutoff if player has a chance to win

        print("end of story")
        return True


                

        


    """
    Safety function : Representation of the pieces proportion that is safe in the current state [0,1]
    # Edges protection : One side of the piece is out of the frame (edge/corner)
    # Color protection : Cells next to the piece have the same color 
    # Opponent color protection : Cells in between two opponent pieces are safe and in an ideal offensive position
    """
    def protectionScore(self, state, color):

        board = state.get_board()

        total = 0

        for x,y in board.get_player_pieces_on_board(color):

            # Safe on edges and corners
            # Maximum score : 4 corners + rest of pieces near edges = 4 + (remaining-4)*0.5
            if x==0 or x==board.board_shape[0]-1:
                total += 0.5
            if y==0 or y==board.board_shape[1]-1:
                total += 0.5

            # Surrounded by pieces of the same color:
            # For each direction :
            # - Protected on one side = +0.5 (therefore +1 = fully protected if both directions)
            # - Protected on the other side = +0.75 (better but not as good as bi-directional protection)
            # Maximum score : When all remaining piece form a perfect rectangular shape, they are all protected = 1*N 

            # x direction
            if x==0 and board.get_cell_color((x+1,y))==color:
                total += 0.5
            elif x==board.board_shape[0]-1 and board.get_cell_color((x-1,y))==color:
                total += 0.5
            else:
                if board.get_cell_color((x-1,y))==color:
                    total += 0.5
                    if board.get_cell_color((x+1,y))==color:
                        total += 0.25
                else:
                    if board.get_cell_color((x+1,y))==color:
                        total += 0.5

            # y direction
            if y==0 and board.get_cell_color((x,y+1))==color:
                total += 0.5
            elif y==board.board_shape[1]-1 and board.get_cell_color((x,y-1))==color:
                total += 0.5
            else:
                if board.get_cell_color((x,y-1))==color:
                    total += 0.5
                    if board.get_cell_color((x,y+1))==color:
                        total += 0.25
                else:
                    if board.get_cell_color((x,y+1))==color:
                        total += 0.5

            # "Protected" by other player's pieces on BOTH sides AND offensive advantage too
            # Very good move evaluated +1.5 (1 for protection, 0.5 for offensive positioning)
            # Maximum score : 1.5*N (estimation)

            # x direction
            if not x==0 and not x==board.board_shape[0]-1:
                cond1 = board.get_cell_color((x-1,y))==color
                cond2 = board.is_empty_cell((x-1, y))==color
                cond3 = board.get_cell_color((x+1,y))==color
                cond4 = board.is_empty_cell((x+1, y))==color
                if (cond1 and cond2) and  (cond3 and cond4):
                    total += 1

            # y direction
            if not y==0 and not y==board.board_shape[1]-1:
                cond1 = board.get_cell_color((x,y-1))==color
                cond2 = board.is_empty_cell((x, y-1))==color
                cond3 = board.get_cell_color((x,y+1))==color
                cond4 = board.is_empty_cell((x, y+1))==color
                if (cond1 and cond2) and  (cond3 and cond4):
                    total += 1

        max_score = 0
        remaining = len(board.get_player_pieces_on_board(color))
        if state.phase==1:
            remaining = (board.board_shape[0]*board.board_shape[1] -1)/2
        

        # Corners and edges
        if remaining <=4:
            max_score += remaining
        else:
            max_score += 4 + (remaining-4)*0.5

        # Self protection
        max_score += remaining 

        # Other player "protection"
        max_score += remaining
        
        return total/max_score #[0,1]


    """
    Check if my player is in center
    """
    def centerControl(self, state, color):
        board = state.board
        my_tiles = board.get_player_pieces_on_board(color)
        if (board.board_shape[0] // 2, board.board_shape[1] // 2) in my_tiles:
            remaining = len(board.get_player_pieces_on_board(color))
            return 1/remaining
        else:
            return 0


    """
    Determine captured tiles
    """
    # Maximum captured = 4
    def capturedScore(self, state):
        captured = state.captured
        max_captured = 4
        if captured is None:
            return 0
        else:
            return len(captured)/max_captured


    """
    Avoid boring moves
    """
    def boringMoves(self, state):
        return state.boring_moves/state.just_stop

        


    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state):

        color = None
        if state.get_latest_player()==self.position:
            color = self.color
        else:
            color = self.opponentColor

        if state.phase == 1:
            value = self.protectionScore(state, color)

            value_f = "{:.4f}".format(value)
            log(f"    = {value_f}")
        else:
            cs = self.capturedScore(state)
            ps = self.protectionScore(state, color)
            cc = self.centerControl(state, color)
            #bm = self.boringMoves(state)
            value = 4*cs + ps + cc #- bm

            cs_f = "{:.4f}".format(cs)
            ps_f = "{:.4f}".format(ps)
            cc_f = "{:.4f}".format(cc)
            #bm_f = "{:.4f}".format(bm)
            value_f = "{:.4f}".format(value)

            log(f"{cs_f}    {ps_f}    {cc_f}    = {value_f}")
            
        return value

    """
    Specific methods for a Seega player (do not modify)
    """

    def set_score(self, new_score):
        self.score = new_score

    def update_player_infos(self, infos):
        self.in_hand = infos['in_hand']
        self.score = infos['score']

    def reset_player_informations(self):
        self.in_hand = 12
        self.score = 0


"""
MiniMax and AlphaBeta algorithms.
Adapted from:
    Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
    Copyright (C) 2014, Universite catholique de Louvain
    GNU General Public License <http://www.gnu.org/licenses/>
"""

inf = float("inf")


def minimax_search(state, player, prune=True):
    """Perform a MiniMax/AlphaBeta search and return the best action.

    Arguments:
    state -- initial state
    player -- a concrete instance of class AI implementing an Alpha-Beta player
    prune -- whether to use AlphaBeta pruning

    """

    def max_value(state, alpha, beta, depth):
        print("Step: Max")
        if player.cutoff(state, depth):
            return player.evaluate(state), None
        val = -inf
        action = None

        for a, s in player.successors(state):
            if s.get_latest_player() == s.get_next_player():  # next turn is for the same player
                v, _ = max_value(s, alpha, beta, depth + 1)
            else:  # next turn is for the other one
                v, _ = min_value(s, alpha, beta, depth + 1)
            if v > val:
                val = v
                action = a
                if prune:
                    if v >= beta:
                        return v, a
                        
                    alpha = max(alpha, v)
        return val, action

    def min_value(state, alpha, beta, depth):
        print("Step: Min")
        if player.cutoff(state, depth):
            return player.evaluate(state), None
        val = inf
        action = None
        for a, s in player.successors(state):
            if s.get_latest_player() == s.get_next_player():  # next turn is for the same player
                v, _ = min_value(s, alpha, beta, depth + 1)
            else:  # next turn is for the other one
                v, _ = max_value(s, alpha, beta, depth + 1)
            if v < val:
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        return v, a
                    beta = min(beta, v)
        return val, action

    v, action = max_value(state, -inf, inf, 0)
    if action==None:
        print("None action in minimax unallowed")
    if not action==None:
        print("Performed action "+str(action.action)+" with value "+str(v))


    return action
