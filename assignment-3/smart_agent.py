
from core.player import Player
from core import Color
from seega.seega_rules import SeegaRules
from copy import deepcopy


class AI(Player):

    in_hand = 12
    score = 0
    name = "Template"

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state, remain_time):
        print("")
        print(f"Player {self.position} is playing.")
        print("time remain is ", remain_time, " seconds")
        return minimax_search(state, self)

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """

    def evaluate_successor(self, successor):
        return self.evaluate(successor[1])

    def successors(self, state):
        actions = SeegaRules.get_player_actions(state, self.position)
        successors = []
        for act in actions:
            new_state = deepcopy(state)
            if SeegaRules.act(new_state, act, self.position):
                successors.append((act, new_state))
        successors.sort(key=self.evaluate_successor)
        return successors


    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):
        if SeegaRules.is_end_game(state):
            return True

        return False

    """
    Safety function : Representation of the pieces proportion that is safe in the current state [0,1]
    # Edges protection : One side of the piece is out of the frame (edge/corner)
    # Color protection : Cells next to the piece have the same color 
    # Opponent color protection : Cells in between two opponent pieces are safe and in an ideal offensive position
    """
    def protectionScore(self, state):

        board = state.get_board()
        total = 0

        for x,y in board.get_player_pieces_on_board(self.color):

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
            if x==0 and board.get_cell_color((x+1,y))==self.color:
                total += 0.5
            elif x==board.board_shape[0]-1 and board.get_cell_color((x-1,y))==self.color:
                total += 0.5
            else:
                if board.get_cell_color((x-1,y))==self.color:
                    total += 0.5
                    if board.get_cell_color((x+1,y))==self.color:
                        total += 0.25
                else:
                    if board.get_cell_color((x+1,y))==self.color:
                        total += 0.5

            # y direction
            if y==0 and board.get_cell_color((x,y+1))==self.color:
                total += 0.5
            elif y==board.board_shape[1]-1 and board.get_cell_color((x,y-1))==self.color:
                total += 0.5
            else:
                if board.get_cell_color((x,y-1))==self.color:
                    total += 0.5
                    if board.get_cell_color((x,y+1))==self.color:
                        total += 0.25
                else:
                    if board.get_cell_color((x,y+1))==self.color:
                        total += 0.5

            # "Protected" by other player's pieces on BOTH sides AND offensive advantage too
            # Very good move evaluated +1.5 (1 for protection, 0.5 for offensive positioning)
            # Maximum score : 1.5*N (estimation)

            # x direction
            if not x==0 and not x==board.board_shape[0]-1:
                cond1 = board.get_cell_color((x-1,y))==self.color
                cond2 = board.is_empty_cell((x-1, y))==self.color
                cond3 = board.get_cell_color((x+1,y))==self.color
                cond4 = board.is_empty_cell((x+1, y))==self.color
                if (cond1 and cond2) and  (cond3 and cond4):
                    total += 1

            # y direction
            if not y==0 and not y==board.board_shape[1]-1:
                cond1 = board.get_cell_color((x,y-1))==self.color
                cond2 = board.is_empty_cell((x, y-1))==self.color
                cond3 = board.get_cell_color((x,y+1))==self.color
                cond4 = board.is_empty_cell((x, y+1))==self.color
                if (cond1 and cond2) and  (cond3 and cond4):
                    total += 1

        max_score = 0
        remaining = len(board.get_player_pieces_on_board(self.color))

        # Corners and edges
        if remaining <=4:
            max_score += remaining
        else:
            max_score += 4 + (remaining-4)*0.5

        # Self protection
        max_score += remaining 

        # Other player protection
        max_score += remaining
        

        return total/max_score #[0,1]


    """
    Check if my player is in center
    """
    def centerControl(self, state):
        board = state.board
        my_tiles = board.get_player_pieces_on_board(self.color)
        if (board.board_shape[0] // 2, board.board_shape[1] // 2) in my_tiles:
            return 1
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
        if state.get_latest_player() == self.position:
            return len(captured)/max_captured
        else:
            return -len(captured)/max_captured

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
        if state.phase == 1:
            value = self.protectionScore(state)
        else:
            cs = self.capturedScore(state)
            ps = self.protectionScore(state)
            cc = self.centerControl(state)
            bm = self.boringMoves(state)
            value = cs + ps + cc + bm
            print(cs,ps,cc,bm)
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

    _, action = max_value(state, -inf, inf, 0)
    return action
