"""
Using a game tree, a safe strategy can be computed:
    Each node in the tree represents a possible state of the game and carries a winning flag.
    winning == 1 means: the player starting with this state has a safe strategy to win.
    winning == -1 means: the player starting with this state will loose, if the opponent plays well.
    winning == 0 means: the flag has not yet been computed.
    Computing the flags starts with setting the flags of the leaves, in the matchTaker game these are the states with
    exactly 1 leaf, their flag is == -1. Then the flags of the predecessor nodes of the leaves are computed, then
    their predecessors are treated etc. until finally the root node is reached. Computing the flag of a node is done
    with the following rule:
        winning = 1 if there is at least 1 successor node with winning == -1, otherwise winning = -1.
    The safe strategy for a node with winning == 1 consists in selecting a move that leads to a successor node
    with winning == -1.
    For a node with winning == -1 all successor nodes have winning == 1 and therefore all moves are "equally useless".
    But it makes sense to choose a move that leaves the game state as complex as possible, in the matchTaker game
    this means having as many matches as possible, i.e. choosing a move that takes only 1 match.

It is not necessary to store all game states in the tree, the normalized states suffice.
Example: [1,0,3,1,2] and [0,2,1,3,1] are both represented by [0,1,1,2,3]. To get the original state back,
the corresponding permutation can be used.

Also, it is much more economical to not use a tree but a dag (directed acyclic graph). Here, each normalized state
occurs only once, and a node may have more than 1 predecessor nodes.
Example: [0,1,1,2,3] has predecessors [1,1,1,2,3], [0,1,2,3,4] and many more.
Although the actual structure is a dag, this module speaks of a "tree", because this is the underlying concept,
the dag is just an optimization.

The tree has a root node. Each node contains a list of all its successor nodes. Thus, from the root all other
nodes can be reached.

The tree has an auxiliary structure, the list of layers. A layer is a list of all nodes having a given total count
of matches. The list of layers is defined such, that the layer at index n contains the nodes having total count of
matches n. Within a layer the nodes are sorted in increasing lexicographic order of the states.
Thus, using the list of layers for any game state the corresponding node can be found quickly.

The module allows the generation of different trees, depending on what is chosen as the root.
The standard game has the root with the state [1,2,3,4,5]. The most trivial game hast the root [0,0,0,0,1]
and its tree contains only 1 node. You can investigate a certain game-state, e.g. [0,1,1,2,2], by generating
the tree with the corresponding root node. The winning flag of the root node will then tell you, whether
you have a safe strategy to win, and if so, the tree will show you the path to victory.
"""

import functools
import bisect
import random

from models.game_states import GameState, GameMove

rand = random.Random()
rand.seed(a=1)  # a=1 for reproducibility


@functools.total_ordering  # generates from == and < the other comparison operators
# GameState ordering is used
# Note: two nodes are considered "equal", when their game_states are equal
#       the winning flag or list of children may be different!
class GameNode:

    def __init__(self, game_state: GameState):
        assert game_state.is_normalized()
        self.game_state = game_state
        self.winning = 0
        self.children = []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.game_state == other.game_state
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.game_state < other.game_state
        else:
            return NotImplemented

    def __str__(self):
        s = f"({self.game_state}w"
        if self.winning == -1:
            s += "-"
        elif self.winning == 1:
            s += "+"
        else:
            s += "0"
        s += f"c:{len(self.children)})"
        return s

    def select_move(self) -> (GameMove, int):
        """ Selects a move leading from self to a new node.
        The value of the winning flag of the new node ist returned, too.
        :return: 0: selected game move
                 1: winning flag of new node
        Assumption: self.winning has been computed already, i.e. != 0
        Note:
            If self.winning == 1, one of the child-nodes with winning == -1 is chosen randomly.
            If self.winning ==-1, one of the child-nodes with winning == 1 and only 1 match less
                                  is chosen randomly
        """
        assert self.winning in [-1, 1]
        if self.winning == 1:
            assert any([child.winning == -1 for child in self.children])
            candidates = [child for child in self.children if child.winning == -1]
        else:
            assert all([child.winning == 1 for child in self.children])
            total_count = self.game_state.get_total_count()
            candidates = [child for child in self.children if child.game_state.get_total_count() == total_count - 1]
        assert len(candidates) > 0
        node = rand.choice(candidates)
        game_move = self.game_state.get_move(node.game_state)
        return game_move, node.winning


class GameLayer:

    def __init__(self, n: int):
        self.n = n
        self.nodes = []

    def insert(self, node: GameNode):
        assert node.game_state.get_total_count() == self.n
        bisect.insort_left(self.nodes, node)

    def find(self, game_state: GameState) -> GameNode or None:
        test_node = GameNode(game_state)
        i = bisect.bisect_left(self.nodes, test_node)
        if i < len(self.nodes) and self.nodes[i] == test_node:
            return self.nodes[i]
        else:
            return None

    def is_sorted_lt(self) -> bool:
        """
        For tests only. Checks that item1 < item2 for any subsequent items.
        :return: True iff all tests passed
        """
        for k in range(len(self.nodes) - 1):
            assert self.nodes[k] < self.nodes[k+1]
        return True


class GameTree:

    def __init__(self, game_state: GameState):
        # for tests and logs only
        self.node_count = 0
        # generate layers
        self.layers = []
        self.total_count = game_state.get_total_count()
        for n in range(self.total_count+1):
            self.layers.append(GameLayer(n))
        # generate root node -- and recursively all nodes
        self.root_node = self._generate_node(game_state)
        # checks
        assert self.node_count == sum([len(layer.nodes) for layer in self.layers])
        assert all([layer.is_sorted_lt() for layer in self.layers])

    def _generate_node(self, game_state: GameState) -> GameNode:
        """
        Generates the node with game_state and also its entire subtree. The node is also inserted into the
        corresponding layer.
        Assumption: a node with game_state does not yet exist in the tree (to avoid empty recursive calls)
        :param game_state: a valid game state, that is a descendant of the root game state
        :return: the generated node
        """
        # init
        assert self.find(game_state) is None
        node = GameNode(game_state)
        # generate all child nodes, look for a winning == -1 flag
        minus1_found = False
        for s_game_state in game_state.normalized_successors():
            s_node = self.find(s_game_state)
            if s_node is None:  # recursive guard
                s_node = self._generate_node(s_game_state)  # recursive call
            node.children.append(s_node)
            assert s_node.winning != 0
            if s_node.winning == -1:
                minus1_found = True
        # set the winning flag
        if minus1_found:
            node.winning = 1
        else:
            node.winning = -1
        # insert this node
        n = game_state.get_total_count()
        self.layers[n].insert(node)
        # count nodes
        self.node_count += 1
        # result
        return node

    def find(self, game_state: GameState) -> GameNode:
        n = game_state.get_total_count()
        assert n <= self.total_count
        node = self.layers[n].find(game_state)
        return node


_current_tree: GameTree


def set_current_tree(game_state: GameState):
    """ Should only be called once by the main program.
    However, unit-tests may call this, too.
    """
    # todo: log warning
    global _current_tree
    _current_tree = GameTree(game_state)


def current_tree() -> GameTree:
    return _current_tree
