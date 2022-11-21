from given_resources.games4e import Game
from test_board import Board


def k_in_row(board, player, square, k):
    """True if player has k pieces in a line through square."""
    def in_row(x, y, dx, dy): return 0 if board[x, y] != player else 1 + in_row(x + dx, y + dy, dx, dy)
    return any(in_row(*square, dx, dy) + in_row(*square, -dx, -dy) - 1 >= k
               for (dx, dy) in ((0, 1), (1, 0), (1, 1), (1, -1)))


class TicTacToe(Game):
    """
    height x width board
    win: k in a row
    X plays first
    """

    def __init__(self, height=3, width=3, k=3):
        self.k = k
        self.squares = {
            (x, y) for x in range(width) for y in range(height)
        }
        self.initial = Board(height=height, width=width, to_move='X', utility=0)

    def actions(self, board):
        return self.squares - set(board)

    def result(self, board, square):
        player = board.to_move
        board = board.new(
            {square: player},
            to_move=('O' if player == 'X' else 'X')
        )
        win = k_in_row(board, player, square, self.k)
        board.utility = (0 if not win else +1 if player == 'X' else -1)
        return board

    def utility(self, board, player):
        return board.utility if player == 'X' else -board.utility

    def is_terminal(self, board):
        return board.utility != 0 or len(self.squares) == len(board)

    def display(self, board): print(board)
