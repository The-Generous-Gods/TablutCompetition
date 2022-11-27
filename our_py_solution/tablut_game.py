"""
Columns and rows counting from 0

Board representation:
    - 9x9 matrix
    - cell content:
        - 0 - no pawn
        - 1 - black pawn
        - 2 - white pawn
        - 3 - king pawn

Move representation (tuple of 2 tuples):
    - ((origin_i, origin_j), (destination_i, destination_j)
"""

import numpy as np
import random

from given_resources.games4e import Game, GameState


class TablutGame(Game):
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    castles = [(4, 4)]
    castle_adjacency = [(3, 4), (4, 3), (5, 4), (4, 5)]

    camps = [
        # UP CAMP
        (0, 3), (0, 4), (0, 5), (1, 4),
        # LEFT CAMP
        (3, 0), (4, 0), (5, 0), (4, 1),
        # RIGHT CAMP
        (3, 8), (4, 8), (5, 8), (4, 7),
        # DOWN CAMP
        (8, 3), (8, 4), (8, 5), (7, 4)
    ]

    camps_adjacency = [
        # UP CAMP
        (1, 3), (2, 4), (1, 5),
        # LEFT CAMP
        (3, 1), (4, 2), (5, 1),
        # RIGHT CAMP
        (3, 7), (4, 6), (5, 7),
        # DOWN CAMP
        (7, 3), (6, 4), (7, 5)
    ]

    escapes = [
        # UP
        (0, 1), (0, 2), (0, 6), (0, 7),
        # LEFT
        (1, 0), (2, 0), (6, 0), (7, 0),
        # RIGHT
        (1, 8), (2, 8), (6, 8), (7, 8),
        # DOWN
        (8, 1), (8, 2), (8, 6), (8, 7)
    ]

    def __init__(self, player):
        player = str(player)
        if "w" in player.lower():
            self.player = "w"
        else:
            self.player = "b"

        board = np.array([
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [1, 0, 0, 0, 2, 0, 0, 0, 1],
            [1, 1, 2, 2, 3, 2, 2, 1, 1],
            [1, 0, 0, 0, 2, 0, 0, 0, 1],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
        ])

        moves = list()
        for (i, j) in np.argwhere(board == 2):
            moves += self.compute_legal_moves(i, j, board)

        self.initial = GameState(
            to_move='w',
            # TODO: INSERT HEURISTIC (HERE PROBABLY 0 CAUSE INITIAL STATE SO EQUAL ODDS)
            utility=0,
            board=board,
            moves=moves
        )

    def actions(self, state):
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state

        new_board = state.board.copy()

        # Compute new board
        (old_i, old_j), (new_i, new_j) = move
        new_board[new_i, new_j] = new_board[old_i, old_j]
        new_board[old_i, old_j] = 0
        new_board = self.eliminate_from_board(new_board, state.to_move, move)

        # Get new moves list
        new_moves = list()
        if state.to_move == 'w':
            for (i, j) in np.argwhere(new_board == 1):
                new_moves += self.compute_legal_moves(i, j, new_board)
        else:
            for (i, j) in np.argwhere(new_board > 1):
                new_moves += self.compute_legal_moves(i, j, new_board)

        return GameState(
            to_move=('w' if state.to_move == 'b' else 'b'),
            utility=self.compute_utility(),
            board=new_board,
            moves=new_moves
        )

    def compute_utility(self):
        # TODO: INSERT HEURISTIC
        return 0

    def utility(self, state, player):
        return 1 if self.player == player else 0
        # return state.utility if self.player == player else -state.utility

    def terminal_test(self, state):
        king_positions = np.argwhere(state.board == 3)
        return \
            len(king_positions) == 0 or \
            tuple(king_positions[0]) in self.escapes or \
            len(state.moves) == 0

    def compute_legal_moves(self, i, j, board):
        moves = list()

        if board[i, j] == 0:
            return moves

        # UP moves
        for i_up in reversed(range(0, i)):
            if ((i, j) not in self.camps) and ((i_up, j) in self.camps):
                break
            if board[i_up, j] == 0:
                moves.append(((i, j), (i_up, j)))
            else:
                break

        # DOWN moves
        for i_down in range(i + 1, board.shape[0]):
            if ((i, j) not in self.camps) and ((i_down, j) in self.camps):
                break
            if board[i_down, j] == 0:
                moves.append(((i, j), (i_down, j)))
            else:
                break

        # LEFT moves
        for j_left in reversed(range(0, j)):
            if ((i, j) not in self.camps) and ((i, j_left) in self.camps):
                break
            if board[i, j_left] == 0:
                moves.append(((i, j), (i, j_left)))
            else:
                break

        # RIGHT moves
        for j_right in range(j + 1, board.shape[1]):
            if ((i, j) not in self.camps) and ((i, j_right) in self.camps):
                break
            if board[i, j_right] == 0:
                moves.append(((i, j), (i, j_right)))
            else:
                break

        final_moves = list()
        for (old_cell, new_cell) in moves:
            if old_cell != (4,4):
                (old_row, old_column) = old_cell
                (new_row, new_column) = new_cell
                if old_row == 4 and new_row == 4:
                    if (old_column <= 4 and new_column >= 4) or (old_column >= 4 and new_column <= 4):
                        continue

                if old_column == 4 and new_column == 4:
                    if (old_row <= 4 and new_row >= 4) or (old_row >= 4 and new_row <= 4):
                        continue
            final_moves.append((old_cell, new_cell))
            
        return final_moves

    def eliminate_from_board(self, board, last_player, move):
        _, (new_i, new_j) = move

        # Eliminate blacks if white move is the last one
        if last_player == 'w':
            for (i_diff, j_diff) in self.neighbors:
                # Basic check
                if 0 < new_i + 2 * i_diff < board.shape[0] - 2 and \
                        0 < new_j + 2 * j_diff < board.shape[1] - 2 and \
                        board[new_i + i_diff, new_j + j_diff] == 1 and \
                        board[new_i + 2 * i_diff, new_j + 2 * j_diff] > 1:
                    board[new_i + i_diff, new_j + j_diff] = 0
                # Castle adjacency
                if (new_i + i_diff, new_j + j_diff) in self.castle_adjacency and \
                        (new_i, new_j) not in self.castles and \
                        board[new_i + i_diff, new_j + j_diff] == 1:
                    board[new_i + i_diff, new_j + j_diff] = 0
                # Camp adjacency
                if (new_i + i_diff, new_j + j_diff) in self.camps_adjacency and \
                        (new_i, new_j) not in self.camps and \
                        board[new_i + i_diff, new_j + j_diff] == 1:
                    board[new_i + i_diff, new_j + j_diff] = 0

        # Eliminate whites if black move is the last one
        if last_player == 'b':
            for (i_diff, j_diff) in self.neighbors:
                # Basic check
                if 0 < new_i + 2 * i_diff < board.shape[0] - 2 and \
                        0 < new_j + 2 * j_diff < board.shape[1] - 2 and \
                        board[new_i + i_diff, new_j + j_diff] > 1 and \
                        board[new_i + 2 * i_diff, new_j + 2 * j_diff] == 1:
                    board[new_i + i_diff, new_j + j_diff] = 0
                # Castle adjacency
                if (new_i + i_diff, new_j + j_diff) in self.castle_adjacency and \
                        (new_i, new_j) not in self.castles and \
                        board[new_i + i_diff, new_j + j_diff] > 1:
                    board[new_i + i_diff, new_j + j_diff] = 0
                # Camp adjacency
                if (new_i + i_diff, new_j + j_diff) in self.camps_adjacency and \
                        (new_i, new_j) not in self.camps and \
                        board[new_i + i_diff, new_j + j_diff] > 1:
                    board[new_i + i_diff, new_j + j_diff] = 0

            if len(np.argwhere(board == 3) > 0):
                # King capture scenarios
                king_position = tuple(np.argwhere(board == 3)[0])
                (king_i, king_j) = king_position
                flag = False
                for (i_os, j_os) in self.neighbors:
                    if (king_i + i_os, king_j + j_os) == (new_i, new_j):
                        flag = True
                        break

                # King in castle
                if flag and king_position in self.castles:
                    if board[3, 4] == board[4, 3] == board[4, 5] == board[5, 4] == 1:
                        board[4, 4] = 0
                # King adjacent to castle
                elif flag and king_position in self.castle_adjacency:
                    enemies_around = 0
                    for neighbor_offset in self.neighbors:
                        neighbor_position = tuple(np.array(king_position) + np.array(neighbor_offset))
                        if board[neighbor_position] == 1:
                            enemies_around += 1
                    if enemies_around == 3:
                        board[king_position] = 0

                # King adjacent to camp
                if flag and king_position in self.camps_adjacency:
                    for neighbor_offset in self.neighbors:
                        neighbor_position = tuple(np.array(king_position) + np.array(neighbor_offset))
                        if neighbor_position not in self.camps:
                            if board[neighbor_position] == 1:
                                board[king_position] = 0
                                break

        return board
