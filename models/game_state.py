"""
    todo: "dummy 0 at index 0" convention. value must be 0, so that sum is not changed
"""

import copy

from utils import permutation


class Error(Exception):
    """Class for exceptions of this module."""

    @classmethod
    def check(cls, condition, *args):
        if not condition:
            raise cls(*args)


class GameState:

    def __init__(self, rows):
        """
        :param rows: a list of integers, representing a valid game state. Otherwise _Error is raised.
        """
        # Check and convert input
        Error.check(isinstance(rows, list), "rows must be a list", "hahaha")
        Error.check(len(rows) == 5, "rows must have length 5")
        self.rows = [0]
        for k in range(5):
            c = rows[k]
            Error.check('0' <= c <= '5', 'rows must consist of digits in 0..5')
            x = int(c)
            Error.check(x <= k+1, f"row {k + 1} must contain <= {k + 1} matches")
            self.rows.append(x)
        Error.check(sum(self.rows) > 0, 'rows must contain at least 1 match')

    def get_rows(self):
        return copy.deepcopy(self.rows)
