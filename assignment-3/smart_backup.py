    """
    Determine the percentage or corner domination
    """
    def check_corners(self, state):
        tot, mine = 4, 0
        board = state.get_board()
        board_shape = board.board_shape[0]
        corners = ((0 ,0), (0 ,board_shape -1), (board_shape -1 ,0), (board_shape -1 ,board_shape -1))
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
        tot, mine = board_shape * 4 -4, 0
        for i in range(board_shape):
            cells = [(0 ,i), (i, 0), (board_shape -1, i), (i, board_shape -1)]
            for c in cells:
                if not board.is_empty_cell(c):
                    if board.get_cell_color(c) == self.color:
                        mine += 1
        return mine /tot

    """
    Determine possible captured tiles proportion
    """
    def check_possible_captured(self, state):
        board = state.get_board()
        board_shape = board.board_shape[0]
        tot, mine, opponent = board_shape *board_shape, 0, 0
        for c in board.get_player_pieces_on_board(self.color):
            if not board.is_empty_cell(c):
                if board.get_cell_color(c) == self.color:
                    x, y = c
                    c1 = ( x -1, y); c2 = ( x +1, y)
                    if board.is_cell_on_board(c1) and board.is_cell_on_board(c2) and \
                            board.get_cell_color(c1) != self.color and board.get_cell_color(c2) != self.color:
                        mine += 1
                    c1 = (x, y- 1);
                    c2 = (x, y + 1)
                    if board.is_cell_on_board(c1) and board.is_cell_on_board(c2) and \
                            board.get_cell_color(c1) != self.color and board.get_cell_color(c2) != self.color:
                        mine += 1
                elif board.get_cell_color(c) != Color.empty:
                    x, y = c
                    c1 = (x - 1, y);
                    c2 = (x + 1, y)
                    if board.is_cell_on_board(c1) and board.is_cell_on_board(c2) and \
                            board.get_cell_color(c1) == self.color and board.get_cell_color(c2) == self.color:
                        opponent += 1
                    c1 = (x, y - 1);
                    c2 = (x, y + 1)
                    if board.is_cell_on_board(c1) and board.is_cell_on_board(c2) and \
                            board.get_cell_color(c1) == self.color and board.get_cell_color(c2) == self.color:
                        opponent += 1
                else:
                    mine += 1
                    opponent += 1
        return mine / tot, opponent / tot

    """
    Determine if the 4 squares in the middle is occuped by the opponent
    """

    def check_cross(self, state):
        x, y = (state.board.board_shape[0] // 2, state.board.board_shape[1] // 2)
        cells = [(x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1)]
        cpt = 0
        for c in cells:
            if state.board.get_cell_color(c) == self.color:
                return 1
        return 0

    """
    Determine if I'm near the center
    """

    def check_near_center(self, state):
        x, y = (state.board.board_shape[0] // 2, state.board.board_shape[1] // 2)
        cells = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for c in cells:
            color = state.board.get_cell_color(c)
            if self.color == color:
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
    Check if my player is in center
    """

    def check_center(self, state):
        board = state.board
        my_tiles = board.get_player_pieces_on_board(self.color)
        if (board.board_shape[0] // 2, board.board_shape[1] // 2) in my_tiles:
            return 1
        else:
            return 0

    """
    Determine empty near black at edge
    """
    def check_empty_near_black(self, state):
        board = state.get_board()
        board_shape = board.board_shape[0]
        mine = 0
        x = 1
        for y in range(1, board_shape-1):
            c1 = board.get_cell_color((x, y))
            c2 = board.get_cell_color((y, x))
            if board.is_empty_cell((x-1, y)) and c1 != self.color and not board.is_empty_cell((x, y)) or board.is_empty_cell((y, x-1)) and c2 != self.color and not board.is_empty_cell((y, x)):
                mine += 1
        x = board_shape-1
        for y in range(1, board_shape-1):
            c1 = board.get_cell_color((x-1, y))
            c2 = board.get_cell_color((y, x-1))
            if board.is_empty_cell((x, y)) and c1 != self.color and not board.is_empty_cell((x-1, y)) or board.is_empty_cell((y, x)) and c2 != self.color and not board.is_empty_cell((y, x-1)):
                mine += 1
        return -mine

    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """

    def evaluate(self, state):
        if state.phase == 1:
            value = self.check_empty_near_black(state) + .25*(self.check_edges(state) + self.check_corners(state)) + self.check_near_center(state)
        else:
            value = self.check_captured(state) + self.check_empty_near_black(state)*self.check_center(state) + self.check_center(state) - self.check_possible_captured(state)[1] + self.check_edges(state) + self.check_corners(state)
        return value