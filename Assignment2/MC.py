import numpy as np
from .utils import (
    is_in, argmin, argmax, argmax_random_tie, probability, weighted_sampler,
    memoize, print_table, open_data, Stack, FIFOQueue, PriorityQueue, name,
    distance
)

class Side:
    def __init__(self, init=0, set=None):
        self.people = ["M", "M", "M", "C", "C", "C"] if init == 1 else set

    def getPeople(self):
        return self.people

    # return 1 if pop is permitted
    # 0 if it is illegal.
    def popPerson(self, p):
        try:
            self.people.remove(p)
            return 1
        except ValueError:
            return -1

    def addPerson(self, p):
        self.people.append(p)

    def getVector(self):
        return [self.people.count("M"), self.people.count("C")]


class Boat:
    def __init__(self):
        self.loc = 1

    def shift(self):
        if self.loc == 1:
            self.loc = 2
        else:
            self.loc = 1


class Environment:
    def __init__(self):
        self.side1 = Side(1)
        self.side2 = Side()
        self.state = np.array([self.side1.getPeople().count("M"),self.side1.getPeople().count("C"),self.side2.getPeople().count("M"),self.side2.getPeople().count("C")])
        self.boat = Boat()
        self.history = []

    def getCurrentState(self):
        self.state = np.array(
            [self.side1.getPeople().count("M"), self.side1.getPeople().count("C"), self.side2.getPeople().count("M"),
             self.side2.getPeople().count("C")])
        return self.state

    def record(self):
        self.getCurrentState()
        self.history.append("Side1: %r, Side2 %r" %(self.side1.getPeople(), self.side2.getPeople()))

class Agent:
    def __int__(self, env):
        # record the wrong state in the side1 in array, which initially is [3,3]
        self.env = env
        self.comb = [["M", "M"], ["C", "C"], ["M", "C"], ["M"], ["C"]]
        self.wrongstate = np.array([env.side1.count("M"), env.side1.count("C")])

    # each step the agent should percept the environment
    def percept(self, env):
        self.env = env

    def shiftBoat(self, load):
        for p in load:
            if self.env.boat == 1:
                self.env.side1.remove(p)
                self.env.boat.shift()
                self.env.side2.append(p)
            else:
                self.env.side2.remove(p)
                self.env.boat.shift()
                self.env.side1.append(p)

    # return TRUE if the state is OK for missionary
    # FALSE if the state is not safe for missionary.
    def checkStateSafe(self, side1, side2):
        for side in [side1, side2]:
            if side.count("C") > side.count("M"):
                return False
        return True

    def checkNextStateSafe(self, comb):
        """
        predict the safety of the possible next move.
        :param comb: list of possible set on the boat
        :return: True for safe, False for unsafe
        """
        temp_side1 = Side(0, self.env.side1.people)
        temp_side2 = Side(0, self.env.side2.people)
        if self.env.boat == 1:
            for p in comb:
                if temp_side1.popPerson(p) == -1:
                    return False
                temp_side2.addPerson(p)
        else:
            for p in comb:
                if temp_side2.popPerson(p) == -1:
                    return False
                temp_side1.addPerson(p)
        return self.checkStateSafe(temp_side1, temp_side2)

    def astar_search(self):
        node = self.env
        if self.goal_test() == True:
            return node
        frontier = PriorityQueue(min, f)


        return 1

    def program(self):
        return 1

    def goal_test(self):
        return self.env.getCurrentState() == np.array([0,0,3,3])

    def heuristcfunction(self):
        self.wrongstate = np.array([self.env.side1.count("M"), self.env.side1.count("C")])


a = np.array([1, 2, 3])
b = np.array([1, 0, 0])
c = [1,2,3,4,5]
env = Environment()
env.record()
print(env.history)