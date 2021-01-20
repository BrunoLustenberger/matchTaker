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
        self.assertFalse(gs.is_normalized())
        p = gs.normalize()
        self.assertTrue(gs.is_normalized())
        self.assertEqual(gs.get_rows(), [0, 1, 1, 2, 3])
        gs.denormalize(p)
        self.assertEqual(gs.get_rows(), rows)


if __name__ == "__main__":
    unittest.main()
