from collections import defaultdict


class Board(defaultdict):
    empty = '.'
    off = '#'

    def __init__(
            self,
            width=3,
            height=3,
            to_move=None,
            **kwds
    ):
        self.__dict__.update(
            width=width,
            height=height,
            to_move=to_move,
            **kwds
        )

    def new(self, changes: dict, **kwds) -> 'Board':
        board = Board(
            width=self.width,
            height=self.height,
            **kwds
        )
        board.update(self)
        board.update(changes)
        return board

    def __missing__(self, loc):
        x, y = loc
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.empty
        else:
            return self.off

    def __hash__(self):
        return hash(tuple(sorted(self.items()))) + hash(self.to_move)

    def __repr__(self):
        def row(y): return ' '.join(self[x, y] for x in range(self.width))
        return '\n'.join(map(row, range(self.height))) + '\n'
