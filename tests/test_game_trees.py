import unittest
import logging

from utils import mylogconfig
from models.game_states import GameState
from models.game_trees import GameNode, GameLayer, GameTree

mylogconfig.standard_rot(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestGameTrees(unittest.TestCase):

    def test_1GameNode(self):
        logger.info("test_1GameNode")
        gs1 = GameState([1, 2, 2, 4, 4])
        gs2 = GameState([1, 2, 3, 3, 4])
        node1 = GameNode(gs1)
        node2 = GameNode(gs2)
        node3 = node2
        node3.winning = -1
        self.assertTrue(node1 < node2)
        self.assertTrue(node2 == node3)
        logger.info(f"node1:{str(node1)}, node2:{str(node2)}, node3:{str(node3)}")

    def test_2GameLayer(self):
        logger.info("test_2GameLayer")
        layer = GameLayer(5)
        self.assertEqual(layer.nodes, [])
        gs1 = GameState([0, 0, 0, 2, 3])  # gs1
        node = layer.find(gs1)
        self.assertTrue(node is None)
        node1 = GameNode(gs1)
        layer.insert(node1)
        node = layer.find(gs1)
        self.assertTrue(node == node1)
        gs2 = GameState([0, 1, 1, 1, 2])  # gs1 < gs2
        node = layer.find(gs2)
        self.assertTrue(node is None)
        node2 = GameNode(gs2)
        layer.insert(node2)
        node = layer.find(gs2)
        self.assertTrue(node == node2)
        gs3 = GameState([0, 0, 0, 0, 5])  # gs3 < gs1
        node = layer.find(gs3)
        self.assertTrue(node is None)
        node3 = GameNode(gs3)
        layer.insert(node3)
        node = layer.find(gs3)
        self.assertTrue(node == node3)
        gs4 = GameState([0, 0, 0, 1, 4])  # gs3 < gs4 < gs1
        node = layer.find(gs4)
        self.assertTrue(node is None)
        node4 = GameNode(gs4)
        layer.insert(node4)
        node = layer.find(gs4)
        self.assertTrue(node == node4)
        gs5 = GameState([1, 1, 1, 1, 1])  # gs3 < gs4 < gs1 < gs2 < gs5
        node = layer.find(gs5)
        self.assertTrue(node is None)
        node5 = GameNode(gs5)
        layer.insert(node5)
        node = layer.find(gs5)
        self.assertTrue(node == node5)
        self.assertTrue(layer.is_sorted_lt())
        logger.info("layer.nodes:"+str(layer.nodes))

    def test_3GameTree(self):
        logger.info("test_3GameTree")
        # the most simple game
        gs = GameState([0, 0, 0, 0, 1])
        tree = GameTree(gs)
        self.assertEqual(tree.node_count, 1)
        self.assertEqual(tree.root_node.winning, -1)
        # some simple situations
        gs = GameState([0, 0, 0, 1, 1])
        tree = GameTree(gs)
        self.assertEqual(tree.node_count, 2)
        self.assertEqual(tree.root_node.winning, 1)
        gs = GameState([0, 0, 1, 1, 1])
        tree = GameTree(gs)
        self.assertEqual(tree.node_count, 3)
        self.assertEqual(tree.root_node.winning, -1)
        gs = GameState([0, 0, 0, 0, 2])
        tree = GameTree(gs)
        self.assertEqual(tree.node_count, 2)
        self.assertEqual(tree.root_node.winning, 1)
        gs = GameState([0, 0, 0, 0, 5])
        tree = GameTree(gs)
        self.assertEqual(tree.node_count, 5)
        self.assertEqual(tree.root_node.winning, -1)
        gs = GameState([0, 0, 0, 2, 3])
        tree = GameTree(gs)
        self.assertEqual(len(tree.layers[4].nodes), 2)
        self.assertEqual(len(tree.layers[3].nodes), 2)
        self.assertEqual(len(tree.layers[2].nodes), 2)
        self.assertEqual(tree.node_count, 8)
        self.assertEqual(tree.root_node.winning, 1)
        gs = GameState([0, 0, 0, 2, 2])
        tree = GameTree(gs)
        self.assertEqual(tree.root_node.winning, -1)
        gs = GameState([0, 1, 1, 2, 2])
        tree = GameTree(gs)
        self.assertEqual(tree.root_node.winning, -1)
        # the "start" situations with 2 to 5 rows
        gs = GameState([0, 0, 0, 1, 2])
        tree = GameTree(gs)
        logger.info("tree root: " + str(tree.root_node) + f" children: {[str(c) for c in tree.root_node.children]}")
        self.assertEqual(tree.node_count, 4)
        self.assertEqual(tree.root_node.winning, 1)
        gs = GameState([0, 0, 1, 2, 3])
        tree = GameTree(gs)
        logger.info("tree root: " + str(tree.root_node) + f" children: {[str(c) for c in tree.root_node.children]}")
        self.assertEqual(len(tree.layers[5].nodes), 3)  # 00023,00113,00122
        self.assertEqual(len(tree.layers[4].nodes), 3)  # 00013,00022,00112
        self.assertEqual(len(tree.layers[3].nodes), 3)  # 00003,00012,00111
        self.assertEqual(len(tree.layers[2].nodes), 2)  # 00002,00011
        self.assertEqual(tree.node_count, 13)
        self.assertEqual(tree.root_node.winning, -1)
        gs = GameState([0, 1, 2, 3, 4])
        tree = GameTree(gs)
        logger.info("tree root: " + str(tree.root_node) + f" children: {[str(c) for c in tree.root_node.children]}")
        logger.info(f"node count: {tree.node_count}")
        logger.info(f"winning: {tree.root_node.winning}")
        gs = GameState([1, 2, 3, 4, 5])
        tree = GameTree(gs)
        logger.info("tree root: " + str(tree.root_node) + f" children: {[str(c) for c in tree.root_node.children]}")
        logger.info(f"node count: {tree.node_count}")
        logger.info(f"winning: {tree.root_node.winning}")


if __name__ == "__main__":
    unittest.main()
