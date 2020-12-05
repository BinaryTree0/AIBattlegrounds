class StateBotrat():
    def __init__(self, state, depth):
        self.state = state
        self.depth = depth
        self.current = -1

    def getCurrentPlayer(self, self):
        self.current = self.current*-1
        return self.current

    def getPossibleActions(self):
        return self.state.getPossibleActions()

    def takeAction(self, action):
        self.state.takeAction(action)

    def isTerminal(self, depth):
        if depth == self.depth:
            return True
        return False

    def getReward(self):
        # only needed for terminal states
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()


class ActionBotrat():
    def __eq__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError()
