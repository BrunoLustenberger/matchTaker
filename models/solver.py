"""


"""
import random
from models.game_states import *

rand = random.Random()
rand.seed(a=1)  # a=1 for reproducibility


class Error(Exception):
    """Class for exceptions of this module."""
    # todo: move to module basic_defs

    @classmethod
    def check(cls, condition, *args):
        if not condition:
            raise cls(*args)


def solve(game_state: GameState, level: int) -> (int, int, int):
    """
    Computes the next move.
    :param game_state: a valid game_state
    :param level: the smartness level
    :return: result[0] row index
             result[1] number of matches to take from this row
             result[2] game continues, int in [-1, 0, 1, 2, 3]
                       -1 : "You won". Occurs when input game_state contained exactly 1 match.
                            In this case, result[0] == 0 and result[1] == 0.
                        0 : "I won". Occurs when game_state after applying result[0] and result[1]
                            contains exactly 1 match.
                        1 : game continues -- no further information
                        2 : game continues -- you have a safe strategy to win
                        3 : game continues -- you have a safe strategy to win
    """
    Error.check(0 <= level <= 2, "level must be an integer in 0..2")
    # init to" you won"
    row_index = 0
    match_count = 0
    game_continues = -1
    rows = game_state.get_rows()

    # sub functions

    def random_move():
        nonlocal row_index, match_count
        non_zeros = [k for k in range(5) if rows[k] > 0]  # all indices with value > 0
        row_index = rand.choice(non_zeros)  # choose such index
        max_n = min(3, rows[row_index])  # max number of matches to be taken at this index
        if len(non_zeros) == 1:  # special case: only this row has matches --> must not take all
            max_n = min(max_n, rows[row_index] - 1)
        match_count = rand.randint(1, max_n)  # choose number of matches at this index

    def most_first():
        nonlocal row_index, match_count
        """ Chooses the row with the most matches and takes as many matches as possible."""
        p = game_state.normalize()
        rows = game_state.get_rows()
        match_count = min(3, rows[4])  # max number of matches
        if rows[3] == 0:  # special case: only this row has matches --> must not take all
            match_count = min(match_count, rows[4] - 1)
        row_index = p.inv()(4)

    # main body continued

    if sum(rows) > 1:
        # choose an algorithm
        if level == 0:
            random_move()
        elif level == 1:
            most_first()
        else:
            pass
        assert 1 <= match_count <= min(3, rows[row_index])
        # check whether I won or game continues
        assert sum(rows) - match_count > 0
        if sum(rows) - match_count > 1:
            game_continues = 1
        else:
            game_continues = 0
    else:
        assert sum(rows) == 1
    return row_index, match_count, game_continues
