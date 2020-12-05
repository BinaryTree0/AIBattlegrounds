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
        newState = deepcopy(self)
        newState.takeAction(action)
        return newState

    def isTerminal(self, depth):
        if depth == self.depth:
            return True
        return False

    def getReward(self):
        return self.state.Wood + self.state.Stone

    def __eq__(self, other):
        raise NotImplementedError()


class ActionBotrat():
    def __eq__(self, other):
        raise NotImplementedError()

    def __hash__(self):
        raise NotImplementedError()
