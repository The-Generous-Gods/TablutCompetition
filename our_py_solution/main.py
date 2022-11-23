from tablut_game import TablutGame
from given_resources.games4e import our_monte_carlo
import numpy as np
import sys
from connect import *


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


def get_params():
    role = sys.argv[1]
    timeout = sys.argv[2]
    ip_address = sys.argv[3]

    if 'w' in role.lower():
        role = 'w'
        port = 5800
    else:
        role = 'b'
        port = 5801

    return role, timeout, ip_address, port


def update_state(new_state):
    """
    Utility function to transform from received state to our representation

    :param new_state:
    :return:
    """
    # Transform to np array in order to work element-wise
    state = np.array(new_state)

    # Transform to our representation
    state[state == "EMPTY"] = 0
    state[state == "BLACK"] = 1
    state[state == "WHITE"] = 2
    state[state == "KING"] = 3

    # Transform from str to int
    state = state.astype("uint8")

    return state


def the_main():
    """
    Current assumption that we only receive legal moves.

    :return:
    """

    # Get params
    role, timeout, ip_address, port = get_params()

    # Help flag
    black = 'b' in role

    # Connect to socket
    client_socket = connect(ip_address, port)

    # Initialize game
    the_game = TablutGame(role)
    current_state = the_game.initial
    tree = None

    # Mandatory first step: sending self name
    send_name(client_socket, role)

    # Receive initial state from server
    # TODO: Maybe check that identical to our (initial) current_state; update otherwise
    received_state = read_state(client_socket)
    # update_state(current_state)

    # White starts so black needs to wait for turn
    if black:
        # Get new state
        received_state = read_state(client_socket)
        # Update stored state
        current_state = update_state(received_state)

    while True:
        # Compute move
        # TODO: Change N back to higher value (currently 10 for testing purposes)
        my_move, tree = compute_move(current_state, the_game, 10, tree)

        # Send our move
        send_action(client_socket, my_move, role)

        # Wait for new move
        received_state = read_state(client_socket)

        # Update with their move
        current_state = update_state(received_state)

        # Update tree according to decision
        tree = tree.children.get(current_state)


if __name__ == '__main__':
    the_main()
