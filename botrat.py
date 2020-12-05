import collections
import numpy as np
import math
from game_logic import play
from heuristics import terminate_fitness

class UCTNode:

    def __init__(
        self,
        game_state,
        move,
        parent=None,
        max_depth = 6,
        ):
        self.game_state = game_state
        self.move = move
        self.depth = parent.depth + 1
        self.max_depth = max_depth
        self.parent = parent  # Optional[UCTNode]
        self.children = {}  # Dict[move, UCTNode]
        self.child_priors = np.zeros([9], dtype=np.float32)
        self.child_total_value = np.zeros([9], dtype=np.float32)
        viable_moves = Heuristic.viable_moves(game_state)
        for i in viable_moves:
            self.child_total_value[i] = -50000
        self.child_number_visits = np.zeros([9], dtype=np.float32)
        if self.depth == max_depth:
            self.reward = Heuristic.reward(self.game_state)
        else:
            self.reward = 0

    @property
    def number_visits(self):
        return self.parent.child_number_visits[self.move]

    @number_visits.setter
    def number_visits(self, value):
        self.parent.child_number_visits[self.move] = value

    @property
    def total_value(self):
        return self.parent.child_total_value[self.move]

    @total_value.setter
    def total_value(self, value):
        self.parent.child_total_value[self.move] = value

    def child_Q(self):
        return self.child_total_value / (1 + self.child_number_visits)

    def child_U(self):
        return np.sqrt(global_time/(self.child_number_visits+1))

    def best_child(self):
        return np.argmax(self.child_Q() + 0.08 *  self.child_U())

    def select_leaf(self):
        current = self
        while current.depth < self.max_depth:
            best_move = current.best_child()
            current = current.maybe_add_child(best_move)
        return current

    def maybe_add_child(self, move):
        if move not in self.children:
            state = self.game_state.copy()
            state.append(move)
            self.children[move] = UCTNode(state, move, parent=self)
        return self.children[move]

    def backup(self, value_estimate):
        current = self
        while current.parent is not None:
            current.number_visits += 1
            current.total_value += value_estimate/self.depth
            current = current.parent


class DummyNode(object):

    def __init__(self):
        self.parent = None
        self.child_total_value = collections.defaultdict(float)
        self.child_number_visits = collections.defaultdict(float)
        self.depth = -1


def UCT_search(num_reads):
    global global_time
    root = UCTNode([], move=None, parent=DummyNode())
    for i in range(num_reads):
        global_time = np.log(np.full((9), i+1))
        leaf = root.select_leaf()
        leaf.backup(leaf.reward)
    return root


class Heuristic:
    @classmethod
    def reward(self, game_state):
        atrs = play(game_state)
        reward = terminate_fitness(atrs)
        return reward
    @classmethod
    def viable_moves(self, game_state):
        return [0]
