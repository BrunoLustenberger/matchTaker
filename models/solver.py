"""


"""
import random
from models.game_states import GameState, GameMove
from models.game_trees import current_tree

rand = random.Random()
rand.seed(a=1)  # a=1 for reproducibility


class Error(Exception):
    """Class for exceptions of this module."""
    # todo: move to module basic_defs

    @classmethod
    def check(cls, condition, *args):
        if not condition:
            raise cls(*args)


def solve(game_state: GameState, level: int) -> (GameMove or None, int):
    """
    Computes the next move.
    :param game_state: a valid game_state
    :param level: the smartness level
    :return: result[0] the game move
             result[1] game continues, int in [-1, 0, 1, 2, 3]
                       -1 : "You won". Occurs when input game_state contained exactly 1 match.
                            In this case, result[0] == None.
                        0 : "I won". Occurs when game_state after making the move result[0]
                            contains exactly 1 match.
                        1 : game continues -- no further information
                        2 : game continues -- you have a safe strategy to win
                        3 : game continues -- your opponent has a safe strategy to win
    """
    Error.check(0 <= level <= 2, "level must be an integer in 0..2")
    rows = game_state.get_rows()

    # sub functions

    def random_move() -> GameMove:
        """ Chooses randomly one of the possible moves."""
        non_zeros = [k for k in range(5) if rows[k] > 0]  # all indices with value > 0
        row_index = rand.choice(non_zeros)  # choose such index
        max_n = min(3, rows[row_index])  # max number of matches to be taken at this index
        if len(non_zeros) == 1:  # special case: only this row has matches --> must not make_move all
            max_n = min(max_n, rows[row_index] - 1)
        match_count = rand.randint(1, max_n)  # choose number of matches at this index
        return GameMove(row_index, match_count)

    def most_first() -> GameMove:
        """ Chooses the row with the most matches and takes as many matches as possible."""
        p = game_state.normalize()
        sorted_rows = game_state.get_rows()
        match_count = min(3, sorted_rows[4])  # max number of matches
        if sorted_rows[3] == 0:  # special case: only this row has matches --> must not take all
            match_count = min(match_count, sorted_rows[4] - 1)
        row_index = p.inv()(4)
        return GameMove(row_index, match_count)

    def best_move() -> (GameMove, int):
        """ Chooses best possible move, if several exist, choose one randomly."""
        p = game_state.normalize()
        node = current_tree().find(game_state)
        _game_move, _winning = node.select_move()
        _game_move.row_index = p.inv()(_game_move.row_index)
        return _game_move, _winning

    # main body continued

    # init to "you won"
    game_move = None
    game_continues = -1
    # not "you won"
    if sum(rows) > 1:
        # choose an algorithm
        winning = 0
        if level == 0:
            game_move = random_move()
        elif level == 1:
            game_move = most_first()
        else:
            game_move, winning = best_move()
        assert 1 <= game_move.match_count <= min(3, rows[game_move.row_index])
        # check whether I won or game continues
        assert sum(rows) - game_move.match_count > 0
        if sum(rows) - game_move.match_count > 1:
            game_continues = 1
            if winning == 1:
                game_continues = 2
            elif winning == -1:
                game_continues = 3
        else:  # I won
            game_continues = 0
    # you won
    else:
        assert sum(rows) == 1
    return game_move, game_continues
