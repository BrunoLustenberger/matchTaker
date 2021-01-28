"""

"""

import copy
import functools

from utils import permutation


class Error(Exception):
    """Class for exceptions of this module."""

    @classmethod
    def check(cls, condition, *args):
        if not condition:
            raise cls(*args)


class GameMove:
    """ A move in the game consists in selecting a row and taking off some matches.
    At least 1 match and at most 3 matches must be taken.
    """

    def __init__(self, row_index: int, match_count: int):
        assert row_index in range(5)
        assert match_count in range(1, 3+1)
        self.row_index = row_index
        self.match_count = match_count

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.row_index == other.row_index and self.match_count == other.match_count
        else:
            return NotImplemented


@functools.total_ordering  # generates from == and < the other comparison operators
# lexicographic ordering is used
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
            Error.check(isinstance(x, int), "rows must contain integers only")
            Error.check(0 <= x <= 5, 'rows must consist of digits in 0..5')
            Error.check(x <= k+1, f"row at index {k} must contain <= {k + 1} matches")
            self.rows.append(x)
        Error.check(sum(self.rows) > 0, 'rows must contain at least 1 match')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.rows == other.rows
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.rows < other.rows
        else:
            return NotImplemented

    def __str__(self):
        s = f"[{self.rows[0]}"
        for k in range(1, len(self.rows)):
            s += f"{self.rows[k]}"
        s += "]"
        return s

    def get_rows(self):
        """ Returns a copy of the internal rows list
        """
        return copy.deepcopy(self.rows)

    def get_total_count(self):
        """ Returns total count of all matches
        """
        return sum(self.rows)

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
            todo: return the inverse, because this is what is being used
        """
        self.rows = p.inv().apply(self.rows)

    def is_possible_move(self, move: GameMove) -> bool:
        """ Returns true iff:
        move.match_count <= number of matches at row_index
        and move.match_count < total count of matches (handles the case, where all matches are in 1 row)
        """
        return (move.match_count <= self.rows[move.row_index]) and (move.match_count < sum(self.rows))

    def make_move(self, move: GameMove):  # -> GameState:
        """ Takes count matches off the row with index k and returns the new game state.
        Assumption: the move is possible.
        """
        assert self.is_possible_move(move)
        new_rows = self.get_rows()
        new_rows[move.row_index] -= move.match_count
        return GameState(new_rows)

    def normalized_successors(self) -> list:
        """
        Assumption: self is a normalized game state.
        :return: list of all normalized game states that can be generated from self with 1 move.
        Example: [0, 0, 1, 2, 2] will return [0, 0, 0, 2, 2], [0, 0, 1, 1, 2], [0, 0, 0, 1, 2]
        """
        assert self.is_normalized()
        result = []
        max_count = min(3, sum(self.rows)-1)
        # later a list of lists may be used, therefore this double loop
        for count in range(1, max_count+1):
            temp = []
            for k in range(5):
                if count <= self.rows[k]:
                    game_state = self.make_move(GameMove(k, count))
                    game_state.normalize()
                    if game_state not in temp:
                        temp.append(game_state)
            result = result + temp
        return result

    # def get_move(self, game_state: GameState) -> (int, int):
    # todo: annotations
    def get_move(self, game_state) -> GameMove:
        """ Returns a move which turns self into a game state, whose normalization is equal to game_state.
        Example: get_move(12345,12235) == (3,2) because 12345 --> 12325 --> 12235
        Assumption: (1) self and game_state are normalized
                    (2) game_state is a successor of self
        :param game_state: the game_state to generate with the move and following normalization
        :return: the move
        """
        assert self.is_normalized()
        assert game_state.is_normalized()
        assert game_state in self.normalized_successors()
        # match_count: the difference of the total counts of matches
        match_count = self.get_total_count() - game_state.get_total_count()
        # row_index: the first from right that has changed
        candidates = [k for k in range(5) if self.rows[k] != game_state.rows[k]]
        assert len(candidates) > 0
        row_index = candidates[-1]
        # check todo: unit-test
        move = GameMove(row_index, match_count)
        temp_state = self.make_move(move)
        temp_state.normalize()
        assert temp_state == game_state
        # return result
        return move
