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
        new_board = self.eliminate_from_board(new_board, state.to_move)

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
        return random.randint(-100, 100)

    def utility(self, state, player):
        return state.utility if self.player == player else -state.utility

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
            # Don't end movement on castle
            if new_cell in self.castles:
                continue

            # Don't end movement on camp
            if (old_cell not in self.camps) and (new_cell in self.camps):
                continue

            final_moves.append((old_cell, new_cell))

        return moves

    def eliminate_from_board(self, board, last_player):
        # Eliminate blacks if white move is the last one
        if last_player == 'w':
            for (i, j) in np.argwhere(board == 1):
                # Vertical basic check
                if 0 < i < board.shape[0] - 1:
                    if board[i - 1, j] == board[i + 1, j] == 2:
                        board[i, j] = 0
                # Horizontal basic check
                if 0 < j < board.shape[1] - 1:
                    if board[i, j - 1] == board[i, j + 1] == 2:
                        board[i, j] = 0
                # Check castle adjacency
                if (i, j) in self.castle_adjacency:
                    rel_pos_i = i - 4
                    rel_pos_j = j - 4

                    if board[i + rel_pos_i, j + rel_pos_j] == 2:
                        board[i, j] = 0
                # Check camp adjacency
                if (i, j) in self.camps_adjacency:
                    for neighbor_offset in self.neighbors:
                        neighbor_position = tuple(np.array((i, j)) + np.array(neighbor_offset))
                        if neighbor_position not in self.camps:
                            if board[neighbor_position] == 1:
                                board[i, j] = 0
                                break

        # Eliminate whites if black move is the last one
        if last_player == 'b':
            for (i, j) in np.argwhere(board == 2):
                # Vertical basic check
                if 0 < i < board.shape[0] - 1:
                    if board[i - 1, j] == board[i + 1, j] == 1:
                        board[i, j] = 0
                # Horizontal basic check
                if 0 < j < board.shape[1] - 1:
                    if board[i, j - 1] == board[i, j + 1] == 1:
                        board[i, j] = 0

                # Check castle adjacency
                if (i, j) in self.castle_adjacency:
                    rel_pos_i = i - 4
                    rel_pos_j = j - 4

                    if board[i + rel_pos_i, j + rel_pos_j] == 1:
                        board[i, j] = 0

            # King capture scenarios
            king_position = tuple(np.argwhere(board == 3)[0])
            # King in castle
            if king_position in self.castles:
                if board[3, 4] == board[4, 3] == board[4, 5] == board[5, 4] == 1:
                    board[4, 4] = 0
            # King adjacent to castle
            elif king_position in self.castle_adjacency:
                enemies_around = 0
                for neighbor_offset in self.neighbors:
                    neighbor_position = tuple(np.array(king_position) + np.array(neighbor_offset))
                    if board[neighbor_position] == 1:
                        enemies_around += 1

                if enemies_around == 3:
                    board[king_position] = 0

            # King adjacent to camp
            if king_position in self.camps_adjacency:
                for neighbor_offset in self.neighbors:
                    neighbor_position = tuple(np.array(king_position) + np.array(neighbor_offset))
                    if neighbor_position not in self.camps:
                        if board[neighbor_position] == 1:
                            board[king_position] = 0
                            break

        return board
