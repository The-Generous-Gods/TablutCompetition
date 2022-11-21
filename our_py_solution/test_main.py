from given_resources.games4e import Game, alpha_beta_search
from test_game import TicTacToe
from test_player import random_player, player


def play_game(game, strategies: dict, verbose=False):
    """Play a turn-taking game. `strategies` is a {player_name: function} dict,
    where function(state, game) is used to get the player's move."""
    state = game.initial
    while not game.is_terminal(state):
        player = state.to_move
        move = strategies[player](state, game)
        state = game.result(state, move)
        if verbose:
            print('Player', player, 'move:', move)
            print(state)
    return state


if __name__ == '__main__':
    role = "white"
    play_game(TicTacToe(), dict(X=random_player, O=player(alpha_beta_search)), verbose=True).utility
    
