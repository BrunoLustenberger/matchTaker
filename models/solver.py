"""


"""
import random
from models.game_states import *

rand = random.Random()
rand.seed(a=1)  # a=1 for reproducibility


class Error(Exception):
    """Class for exceptions of this module."""

    @classmethod
    def check(cls, condition, *args):
        if not condition:
            raise cls(*args)


def solve(game_state: GameState, level: int) -> (int, int, bool):
    """
    Computes the next move.
    :param game_state: a valid game_state
    :param level: the smartness level
    :return: result[0] row index
             result[1] number of matches to take from this row
             result[2] game continues:
                       True  : game continues
                       False : game ended
                               Case 1: "You won". Occurs when game_state contained exactly 1 match.
                                       In this case, result[0] == 0 and result[1] == 0
                               Case 2: "I won". Occurs when game_state after applying result[0] and result[1]
                                       contains exactly 1 match
    """
    Error.check(0 <= level <= 2, "level must be an integer in 0..2")
    # init to game ended case 1
    row_index = 0
    match_count = 0
    game_continues = False
    rows = game_state.get_rows()
    if sum(rows) > 1:
        # choose an algorithm
        if level == 0:
            row_index, match_count = random_move(rows)
        elif level == 1:
            row_index, match_count = most_first(game_state)
        else:
            pass
        # check whether game ended case 2 holds
        assert sum(rows) - match_count > 0
        game_continues = (sum(rows) - match_count > 1)
    else:
        assert sum(rows) == 1
    return row_index, match_count, game_continues


def random_move(rows):
    """ Sub function of solver, parameters see there
    """
    non_zeros = [k for k in range(5) if rows[k] > 0]  # all indices with value > 0
    row_index = rand.choice(non_zeros)  # choose such index
    max_n = min(3, rows[row_index])  # max number of matches to be taken at this index
    if len(non_zeros) == 1:  # special case: only this row has matches --> must not take all
        max_n = min(max_n, rows[row_index] - 1)
    match_count = rand.randint(1, max_n)  # choose number of matches at this index
    return row_index, match_count


def most_first(game_state):
    """ Sub function of solver, parameters see there
        Chooses the row with the most matches and takes as many matches as possible.
    """
    p = game_state.normalize()
    rows = game_state.get_rows()
    match_count = min(3, rows[4])  # max number of matches
    if rows[3] == 0:  # special case: only this row has matches --> must not take all
        match_count = min(match_count, rows[4] - 1)
    row_index = p.inv()(4)
    return row_index, match_count
