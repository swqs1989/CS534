import numpy as np
class Agent:
    def __init__(self):
        self.comb = [np.array([2,0]), np.array([0,2]), np.array([1,1]), np.array([1,0]), np.array([0,1])]
        self.history = []
        self.search_used = 0

    def shiftboat(self, nparray, load):
        """
        make the boat and people shift
        :param load: np.array of 6 elements
        :param load: np.array of 2 elements
        :return: True if successfully else False
        """
        target = nparray.copy()
        if target[2] == 1:
            target[0:2] -= load
            target[3:5] += load
        else:
            target[0:2] += load
            target[3:5] -= load
        target[2], target[5] = target[5], target[2]
        #print(target)
        return target

    def checkfeasible(self, nparray, comb):
        """
        check if the next step is feasible
        :param nparray: current state
        :param comb: possible action
        :return: true if feasible
        """
        target = nparray.copy()
        if target[2] == 1:
            target[0:2] -= comb
            target[3:5] += comb
        else:
            target[0:2] += comb
            target[3:5] -= comb
        target[2], target[5] = target[5], target[2]
        return self.checkState(target) and self.checksafety(target)

    def checkState(self, nparray):
        """
        check if the state is legal
        :param nparray: np.array of 6 elements
        :return:
        """
        if all(i >= 0 for i in nparray):
            return True
        else:
            return False

    def checksafety(self, nparray):
        """
        check if the missionary is safe.
        :param nparray: np.array of 6 elements
        :return:
        """
        if (nparray[0] >= nparray[1] or nparray[0] == 0) and (nparray[3] >= nparray[4] or nparray[3] == 0):
            return True
        else:
            return False

    def goal_test(self, target):
        if np.array_equal(target, np.array([0,0,0,3,3,1])):
            return True
        else:
            return False

    def heuristicfunction(self, nparray):
        return 6 - nparray[3] - nparray[4]

    def performance(self):
        return self.search_used

    def astar_search(self, state, explored=[[3,3,1,0,0,0]]):
        self.search_used += 1
        if self.goal_test(state):
            for ex in explored:
                print(ex)
            print(state)
            return state
        for comb in self.comb:
            if self.checkfeasible(state, comb):
                newstate = self.shiftboat(state, comb)
                # print("second")
                if newstate.tolist() not in explored:
                    #print(newstate)
                    explored.append(newstate.tolist())
                    self.astar_search(newstate, explored)



agent = Agent()
agent.astar_search(np.array([3,3,1,0,0,0]))
print("Number of search used: %r" %agent.search_used)
# a = np.array([1,2]).tolist()
# b = np.array([2,1]).tolist()
#
# c = []
#
# c.append(a)
#
# if b in c:
#     print("A")