import unittest
import logging

from utils import mylogconfig
from models.game_states import *

mylogconfig.standard_rot(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestGameState(unittest.TestCase):

    def test_1init(self):
        logger.info("test_1init")
        try:
            GameState('12345')
            self.assertTrue(False)
        except Error:
            pass
        try:
            GameState(list('123'))
            self.assertTrue(False)
        except Error:
            pass
        try:
            GameState([1, 2, 3, 'a', 5])
            self.assertTrue(False)
        except Error:
            pass
        try:
            GameState([0, 3, 4, 5, 5])
            self.assertTrue(False)
        except Error:
            pass
        try:
            GameState([1, 3, 3, 4, 5])
            self.assertTrue(False)
        except Error:
            pass
        try:
            GameState([0, 0, 0, 0, 0])
            self.assertTrue(False)
        except Error:
            pass

    def test_2normalize(self):
        logger.info("test_2normalize")
        rows = [1, 0, 3, 2, 1]
        gs = GameState(rows)
        self.assertEqual(gs.get_rows(), rows)
        self.assertEqual(str(gs),"[10321]")
        self.assertFalse(gs.is_normalized())
        p = gs.normalize()
        self.assertTrue(gs.is_normalized())
        self.assertEqual(gs.get_rows(), [0, 1, 1, 2, 3])
        gs.denormalize(p)
        self.assertEqual(gs.get_rows(), rows)

    def test_3ordering(self):
        logger.info("test_3ordering")
        gs_max = GameState([1, 2, 3, 4, 5])
        gs1 = GameState([1, 0, 0, 0, 0])
        gs2 = GameState([0, 1, 0, 0, 0])
        gs_min = GameState([0, 0, 0, 0, 1])
        self.assertTrue(gs_min < gs2)
        self.assertTrue(gs2 < gs1)
        self.assertTrue(gs1 < gs_max)
        gs3 = GameState([1, 2, 0, 4, 0])
        gs4 = GameState([1, 1, 3, 4, 5])
        self.assertTrue(gs_min < gs4 < gs3 < gs_max)
        self.assertTrue(gs_min <= gs4 <= gs3 <= gs_max)

    def test_4successors_and_take(self):
        logger.info("test_4successors_and_take")
        self.assertEqual(GameState([1, 2, 3, 4, 5]).take(2, 1), GameState([1, 0, 3, 4, 5]))
        self.assertEqual(GameState([0, 0, 0, 3, 0]).take(2, 3), GameState([0, 0, 0, 1, 0]))
        self.assertEqual(GameState([1, 0, 0, 3, 0]).take(1, 0), GameState([0, 0, 0, 3, 0]))
        self.assertEqual(GameState([0, 0, 0, 0, 1]).normalized_successors(), [])
        self.assertEqual(sorted(GameState([0, 0, 0, 0, 3]).normalized_successors()),
                         sorted([GameState([0, 0, 0, 0, 2]), GameState([0, 0, 0, 0, 1])]))
        self.assertEqual(sorted(GameState([0, 0, 1, 2, 2]).normalized_successors()),
                         sorted([GameState([0, 0, 0, 2, 2]), GameState([0, 0, 1, 1, 2]), GameState([0, 0, 0, 1, 2])]))
        self.assertEqual(len(GameState([1, 2, 3, 4, 5]).normalized_successors()), 5+4+3)
        self.assertEqual(sorted(GameState([1, 2, 3, 4, 5]).normalized_successors()),
                         sorted([GameState([0, 2, 3, 4, 5]), GameState([1, 1, 3, 4, 5]), GameState([1, 2, 2, 4, 5]),
                                 GameState([1, 2, 3, 3, 5]), GameState([1, 2, 3, 4, 4]),
                                 GameState([0, 1, 3, 4, 5]), GameState([1, 1, 2, 4, 5]), GameState([1, 2, 2, 3, 5]),
                                 GameState([1, 2, 3, 3, 4]),
                                 GameState([0, 1, 2, 4, 5]), GameState([1, 1, 2, 3, 5]), GameState([1, 2, 2, 3, 4])
                                 ]))


if __name__ == "__main__":
    unittest.main()
