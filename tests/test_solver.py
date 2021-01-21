import unittest
import logging

from utils import mylogconfig
import models
from models.solver import solve
from models.game_states import GameState

""" following code doesn't work for debugger --> uncomment
"""
mylogconfig.standard_rot(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestSolver(unittest.TestCase):

    def all_levels(self, level):
        gs = GameState([0, 0, 1, 0, 0])
        row_i, count, cont = solve(gs, level)
        self.assertTrue(row_i == 0 and count == 0 and cont == -1)
        gs = GameState([1, 0, 1, 0, 0])
        row_i, count, cont = solve(gs, level)
        self.assertTrue(row_i in [0, 2] and count == 1 and cont == 0)
        gs = GameState([0, 0, 3, 0, 0])
        row_i, count, cont = solve(gs, level)
        self.assertTrue(row_i == 2 and 1 <= count <= 2 and ((count == 1) == (cont > 0)))

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
        row_i, count, cont = solve(gs, 0)
        self.assertTrue(row_i in [3, 4] and 1 <= count <= 3 and cont > 0)

    def test_3most_first(self):
        self.all_levels(1)
        gs = GameState([1, 2, 3, 4, 5])
        row_i, count, cont = solve(gs, 1)
        self.assertTrue(row_i == 4 and count == 3 and cont == 1)
        gs = GameState([0, 0, 3, 2, 1])
        row_i, count, cont = solve(gs, 1)
        self.assertTrue(row_i == 2 and count == 3 and cont == 1)
        gs = GameState([0, 2, 1, 1, 1])
        row_i, count, cont = solve(gs, 1)
        self.assertTrue(row_i == 1 and count == 2 and cont == 1)
        gs = GameState([0, 2, 0, 0, 1])
        row_i, count, cont = solve(gs, 1)
        self.assertTrue(row_i == 1 and count == 2 and cont == 0)


if __name__ == "__main__":
    unittest.main()
