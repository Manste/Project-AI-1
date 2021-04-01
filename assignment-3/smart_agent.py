

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
        self.depth = 0

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
    def successors(self, state):
        return self.get_successors(state, self.position)

    def get_successors(self, state, color):
        actions = SeegaRules.get_player_actions(state, color)
        for act in actions:
            new_state = deepcopy(state)
            if SeegaRules.act(new_state, act, color):
                self.depth += 1
                yield (act, new_state)

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):
        if SeegaRules.is_end_game(state) or self.depth <= depth != 0:
            self.depth = 0
            return True
        return False


    """
    Determine the percentage or corner domination
    """
    def check_corners(self, state):
        tot, mine = 4, 0
        board = state.get_board()
        board_shape = board.board_shape[0]
        corners = ((0,0), (0,board_shape-1), (board_shape-1,0), (board_shape-1,board_shape-1))
        for c in corners:
            if not board.is_empty_cell(c):
                if board.get_cell_color(c) == self.color:
                    mine += 1
        return mine/tot

    """
    Determine edge controls proportions
    """
    def check_edges(self, state):
        board = state.get_board()
        board_shape = board.board_shape[0]
        tot, mine = board_shape*4-4, 0
        for i in range(board_shape):
            cells = [(0,i), (i, 0), (board_shape-1, i), (i, board_shape-1)]
            for c in cells:
                if not board.is_empty_cell(c):
                    if board.get_cell_color(c) == self.color:
                        mine += 1
        return mine/tot

    """
    Determine possible captured tiles proportion
    """
    def check_possible_captured(self, state):
        board = state.get_board()
        board_shape = board.board_shape[0]
        tot, mine, opponent = board_shape*board_shape, 0, 0
        for c in board.get_player_pieces_on_board(self.color):
            if not board.is_empty_cell(c):
                if board.get_cell_color(c) == self.color:
                    x, y = c
                    c1 = (x-1, y); c2 = (x+1, y)
                    if board.is_cell_on_board(c1) and board.is_cell_on_board(c2) and \
                            board.get_cell_color(c1) != self.color and board.get_cell_color(c2) != self.color:
                        mine += 1
                    c1 = (x, y-1); c2 = (x, y+1)
                    if board.is_cell_on_board(c1) and board.is_cell_on_board(c2) and \
                            board.get_cell_color(c1) != self.color and board.get_cell_color(c2) != self.color:
                        mine += 1
                elif board.get_cell_color(c) != Color.empty:
                    x, y = c
                    c1 = (x-1, y); c2 = (x+1, y)
                    if board.is_cell_on_board(c1) and board.is_cell_on_board(c2) and \
                            board.get_cell_color(c1) == self.color and board.get_cell_color(c2) == self.color:
                        opponent += 1
                    c1 = (x, y-1); c2 = (x, y+1)
                    if board.is_cell_on_board(c1) and board.is_cell_on_board(c2) and \
                            board.get_cell_color(c1) == self.color and board.get_cell_color(c2) == self.color:
                        opponent += 1
        return -mine/tot, opponent/tot

    """
    Determine if the 4 squares in the middle is occuped by the opponent
    """
    def check_cross(self, state):
        x, y = (state.board.board_shape[0] // 2, state.board.board_shape[1] // 2)
        cells = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        for c in cells:
            color = state.board.get_cell_color(c)
            if self.color == color or color == Color.empty:
                return 1
        return 0

    """
    Determine captured tiles
    """
    def check_captured(self, state):
        captured = state.captured
        if captured is None:
            return 0
        if state.get_latest_player() == self.position:
            return len(captured)
        else:
            return -len(captured)

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state):
        if state.phase == 1:
            return self.check_cross(state)
        else:
            return self.check_captured(state)

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
            else:                                             # next turn is for the other one
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
            else:                                             # next turn is for the other one
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

