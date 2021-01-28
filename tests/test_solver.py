import unittest
import logging

from utils import mylogconfig
import models
from models.solver import solve
from models.game_states import GameState
from models.game_trees import set_current_tree

""" following code doesn't work for debugger --> uncomment
"""
mylogconfig.standard_rot(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestSolver(unittest.TestCase):

    def all_levels(self, level):
        gs = GameState([0, 0, 1, 0, 0])
        gm, cont = solve(gs, level)
        self.assertTrue(gm is None and cont == -1)
        gs = GameState([1, 0, 1, 0, 0])
        gm, cont = solve(gs, level)
        self.assertTrue(gm.row_index in [0, 2] and gm.match_count == 1 and cont == 0)
        gs = GameState([0, 0, 3, 0, 0])
        gm, cont = solve(gs, level)
        self.assertTrue(gm.row_index == 2 and 1 <= gm.match_count <= 2 and ((gm.match_count == 1) == (cont > 0)))

    def test_1init(self):
        gs = GameState([1, 2, 3, 4, 5])
        try:
            solve(gs, 3)
            self.assertTrue(False)
        except models.solver.Error:
            pass

    def test_2random(self):
        self.all_levels(0)
        gs = GameState([0, 0, 0, 4, 5])
        gm, cont = solve(gs, 0)
        self.assertTrue(gm.row_index in [3, 4] and 1 <= gm.match_count <= 3 and cont > 0)

    def test_3most_first(self):
        self.all_levels(1)
        gs = GameState([1, 2, 3, 4, 5])
        gm, cont = solve(gs, 1)
        self.assertTrue(gm.row_index == 4 and gm.match_count == 3 and cont == 1)
        gs = GameState([0, 0, 3, 2, 1])
        gm, cont = solve(gs, 1)
        self.assertTrue(gm.row_index == 2 and gm.match_count == 3 and cont == 1)
        gs = GameState([0, 2, 1, 1, 1])
        gm, cont = solve(gs, 1)
        self.assertTrue(gm.row_index == 1 and gm.match_count == 2 and cont == 1)
        gs = GameState([0, 2, 0, 0, 1])
        gm, cont = solve(gs, 1)
        self.assertTrue(gm.row_index == 1 and gm.match_count == 2 and cont == 0)

    def test_4best(self):
        set_current_tree(GameState([1, 2, 3, 4, 5]))
        self.all_levels(2)
        # winning states
        gs = GameState([0, 2, 1, 1, 1])
        gm, cont = solve(gs, 2)
        self.assertTrue(gm.row_index == 1 and gm.match_count == 2 and cont == 3)
        gs = GameState([1, 2, 3, 4, 5])  # see logs of 12345 in test_game_trees
        gm, cont = solve(gs, 2)
        self.assertTrue(cont == 3)
        # looser states
        gs = GameState([0, 1, 1, 0, 1])
        gm, cont = solve(gs, 2)
        self.assertTrue(gm.match_count == 1 and cont == 2)
        gs = GameState([1, 2, 0, 4, 3])  # see logs of 01234 in test_game_trees
        gm, cont = solve(gs, 2)
        self.assertTrue(gm.match_count == 1 and cont == 2)


if __name__ == "__main__":
    unittest.main()
