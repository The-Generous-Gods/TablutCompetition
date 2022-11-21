from tablut_game import TablutGame
from given_resources.games4e import our_monte_carlo
import numpy as np
import sys


def get_move_from_state_diff(old_board, new_board):
    changes = np.argwhere(old_board != new_board)

    if old_board[changes[0]] != 0:
        return tuple(changes[0]), tuple(changes[1])
    else:
        return tuple(changes[1]), tuple(changes[0])


def compute_move(state, game, max_steps, tree):
    # TODO: maybe modify instead of max_steps give max_time or keep max_steps if constant ish
    tree = our_monte_carlo(state, game, max_steps, tree)
    move = get_move_from_state_diff(state.board, tree.state.board)
    return move, tree


def send(move):
    # TODO: OBVIOUSLY
    return "SENDING"


def wait():
    # TODO: OBVIOUSLY
    return "WAITING"


def the_main(role, time_out, address):
    # TODO: Connect with json
    # Initialize game
    the_game = TablutGame(role)
    current_state = the_game.initial
    tree = None

    while True:
        if current_state.to_move == role:
            my_move, tree = compute_move(current_state, the_game, 1000, tree)
            current_state = the_game.result(current_state, my_move)
            send(my_move)
        else:
            their_move = wait()
            current_state = the_game.result(current_state, their_move)
            tree = tree.children.get(current_state)

    # TODO: Check OneNote and rules once again to check that it's all


if __name__ == '__main__':
    role = sys.argv[1]
    time_out = sys.argv[2]
    address = sys.argv[3]

    if "w" in role.lower():
        role = "w"
    else:
        role = "b"

    # the_main(role, time_out, address)
