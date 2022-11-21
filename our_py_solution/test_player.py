import random


def random_player(state, game):
    return random.choice(list(game.actions(state)))


def player(search_algorithm):
    return lambda game, state: search_algorithm(game, state)[1]
