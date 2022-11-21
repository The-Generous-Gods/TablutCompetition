from tablut_game import TablutGame
from given_resources.games4e import monte_carlo_tree_search


def compute_move(state, game, max_steps):
    # TODO: modify in such a way as to save the tree from one step to another
    # TODO: modify in such a way as to avoid repetitive nodes
    # TODO: modify instead of max_steps give max_time
    return monte_carlo_tree_search(state, game, max_steps)


def send(move):
    # TODO: OBVIOUSLY
    return "SENDING"


def wait():
    # TODO: OBVIOUSLY
    return "WAITING"


if __name__ == '__main__':
    # TODO: Bash initialization
    role = "w"
        # TODO: Method to get role from given arguments
        # TODO: Connect with json
        # TODO: Other stuff from bash

    # Initialize game
    the_game = TablutGame(role)
    current_state = the_game.initial

    while True:
        if current_state.to_move == role:
            my_move = compute_move(current_state, the_game, 1000)
            current_state = the_game.result(current_state, my_move)
            send(my_move)
        else:
            their_move = wait()
            current_state = the_game.result(current_state, their_move)

    # TODO: Check OneNote and rules once again to check that it's all
