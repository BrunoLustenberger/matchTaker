"""

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
        """ Creates a game state.
            param rows: a list of integers, representing a valid game state. Otherwise Error is raised.
        """
        # Check and convert input
        Error.check(isinstance(rows, list), "rows must be a list", "hahaha")
        Error.check(len(rows) == 5, "rows must have length 5")
        self.rows = []
        for k in range(5):
            x = rows[k]
            Error.check(isinstance(x,int), "rows must contain integers only")
            Error.check(0 <= x <= 5, 'rows must consist of digits in 0..5')
            Error.check(x <= k+1, f"row at index {k} must contain <= {k + 1} matches")
            self.rows.append(x)
        Error.check(sum(self.rows) > 0, 'rows must contain at least 1 match')

    def get_rows(self):
        """ Returns a copy of the internal rows list
        """
        return copy.deepcopy(self.rows)

    def normalize(self):
        """ Sorts the internal rows list and returns the permutation generating this sort order.
        """
        self.rows, p = permutation.Permutation.sorted(self.rows)
        return p

    def is_normalized(self):
        """ Returns True iff the internal rows list ist sorted in ascending order. """
        test_list = [self.rows[k] <= self.rows[k+1] for k in range(4)]
        return all(test_list)

    def denormalize(self, p):
        """ Resets the internal rows list to state before normalization.
            Param p: The permutation that was returned by the call to normalize()
        """
        self.rows = p.inv().apply(self.rows)
