import collections
import numpy as np
import math

features = 9

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
        self.child_priors = np.zeros([features], dtype=np.float32)
        self.child_total_value = np.zeros([features], dtype=np.float32)
        self.child_number_visits = np.zeros([features], dtype=np.float32)
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

    def expand(self, child_priors):
        self.child_priors = child_priors

    def maybe_add_child(self, move):
        if move not in self.children:
            self.children[move] = UCTNode(self.game_state.play(move), move, parent=self)
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


def UCT_search(game_state, num_reads):
    global global_time
    root = UCTNode(game_state, move=None, parent=DummyNode())
    for i in range(num_reads):
        global_time = np.log(np.full((features), i+1))
        leaf = root.select_leaf()
        child_priors = Heuristic.priors(leaf.game_state)
        leaf.expand(child_priors)
        leaf.backup(leaf.reward)
    return root


class Heuristic:
    @classmethod
    def priors(self, game_state):
        return np.random.random([features])
    @classmethod
    def reward(self, game_state):
        return np.random.random()-0.5


class GameState:

    def __init__(self, to_play=1):
        self.to_play = to_play

    def play(self, move):
        return GameState(-self.to_play)


num_reads = 50000
import time
tick = time.time()
root = UCT_search(GameState(), num_reads)
tock = time.time()
print("Took %s sec to run %s times" % (tock - tick, num_reads))
import resource
print("Consumed %sB memory" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
curr = root
while curr.depth<=5:
    move = np.argmax(curr.child_total_value)
    curr = curr.children[move]

curr = curr.parent
print(root.child_number_visits)
print(root.child_total_value)
print("Rewards:",end=" ")
for i in curr.children.values():
    print(i.reward,end=", ")
