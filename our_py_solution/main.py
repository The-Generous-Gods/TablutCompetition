from tablut_game import TablutGame
from given_resources.games4e import our_monte_carlo, monte_carlo_tree_search, GameState
import numpy as np
import sys
from connect import *


def get_move_from_state_diff(old_board, new_board, role):
    if 'w' in role:
        old_board = old_board * (old_board > 1).astype("uint8")
        new_board = new_board * (new_board > 1).astype("uint8")
    else:
        old_board = old_board * (old_board == 1).astype("uint8")
        new_board = new_board * (new_board == 1).astype("uint8")

    changes = np.argwhere(old_board != new_board)

    if old_board[tuple(changes[0])] != 0:
        return tuple(changes[0]), tuple(changes[1])
    else:
        return tuple(changes[1]), tuple(changes[0])


def compute_move(state, game, max_steps, tree):
    # TODO: maybe modify instead of max_steps give max_time or keep max_steps if constant ish
    return monte_carlo_tree_search(state, game, max_steps)
    # return our_monte_carlo(state, game, max_steps, tree)


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


def update_state(new_board, old_state, game, role):
    """
    Utility function to transform from received state to our representation

    :param new_state:
    :return:
    """
    # Transform to np array in order to work element-wise
    new_board = np.array(new_board)

    # Transform to our representation
    new_board[new_board == "EMPTY"] = 0
    new_board[new_board == "BLACK"] = 1
    new_board[new_board == "WHITE"] = 2
    new_board[new_board == "KING"] = 3
    new_board[new_board == "THRONE"] = 0

    # Transform from str to int
    new_board = new_board.astype("uint8")

    # Compute move
    # the_move = get_move_from_state_diff(old_state.board, new_board, 'w' if 'b' in role else 'b')

    moves = list()
    if role == 'b':
        for (i, j) in np.argwhere(new_board == 1):
            moves += game.compute_legal_moves(i, j, new_board)
    else:
        for (i, j) in np.argwhere(new_board > 1):
            moves += game.compute_legal_moves(i, j, new_board)

    # return game.result(old_state, the_move)
    return GameState(
            to_move=role,
            utility=game.compute_utility(),
            board=new_board,
            moves=moves
    )


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
    received_state, received_mover = read_state(client_socket)
    # update_state(current_state)

    # White starts so black needs to wait for turn
    if black:
        # Get new state
        received_state, received_mover = read_state(client_socket)
        # Update stored state
        current_state = update_state(received_state, current_state, the_game, role)

    time = (int(timeout)/10)-1

    while True:
        # Compute move
        # TODO: Change N back to higher value (currently 10 for testing purposes)
        
        my_move = compute_move(current_state, the_game, time, tree)

        # Update stored state
        current_state = the_game.result(current_state, my_move)

        # Send our move
        send_action(client_socket, my_move, role)

        # Receive result of our move
        _ = read_state(client_socket)

        # Wait for new move
        received_state, received_mover = read_state(client_socket)

        # Update with their move
        current_state = update_state(received_state, current_state, the_game, role)

        # Update tree according to decision
        # tree = tree.children.get(current_state)


if __name__ == '__main__':
    the_main()
