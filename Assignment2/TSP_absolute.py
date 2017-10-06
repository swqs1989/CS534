import random as ra
from heapq import heappush, heapify, heappop
import itertools
import math

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "%r, %r" %(self.x, self.y)

class TSP:
    def __init__(self, dictmap=None, city=None, visted=None, unvisted=None, cost=None, parent=None):
        # self.map = {0: City(12, 1), 1: City(2, 12), 2: City(89, 19), 3: City(77,24), 4: City(1, 11), 5: City(0, 9), 6: City(91, 79), 7: City(99, 43), 8: City(55, 49), 9: City(14, 99)} if dictmap is None else dictmap
        self.map = {0: City(23, 1), 1: City(7, 12), 2: City(8, 19), 3: City(99,24), 4: City(0, 84), 5: City(45, 9)} if dictmap is None else dictmap
        self.current = city if city is not None else self.map[0]
        self.visited = visted if visted is not None else [self.map[0]]
        self.unvisted = unvisted if unvisted is not None else [self.map[i] for i in range(1, len(self.map))]
        self.cost = cost if cost is not None else 0
        self.parent = parent if parent is not None else None
        self.score = self.funcf()

    def getresult(self):
        # City(23, 1)
        mini = 9999999
        results = []
        cities = [City(7, 12), City(8, 19), City(99,24), City(0, 84), City(45, 9), City(31, 42), City(93,44), City(9,99), City(21,11), City(67,12), City(87,56), City(33,44)]
        for value in itertools.permutations(cities, len(cities)):
            result = 0

            for i in range(len(value)):
                if i == 0:
                    result += distance(City(23, 1), value[0])
                else:
                    result += distance(value[i], value[i-1])
            result += distance(City(23, 1), value[len(value) - 1])
            # results.append(result)
            mini = min(result, mini)
        # for v in results:
        #     print(v)

        return mini





    def gennextstep(self):
        for city in self.unvisted:
            visted = self.visited.copy()
            unvisted = self.unvisted.copy()
            visted.append(city)
            unvisted.remove(city)
            cost = self.cost + distance(self.current, city)
            yield TSP(None, city, visted, unvisted, cost, self)

    def funch(self):
        total = 0
        unvisted = self.unvisted.copy()

        if len(unvisted) > 0:
            visted = []
            visted.append(unvisted.pop())
            while unvisted:
                city = None
                target = None
                for c in visted:
                    for d in unvisted:
                        # target = min(distance(c, d), target) if target is not None else distance(c, d)
                        if target == None:
                            target = distance(c, d)
                            city = d
                        if distance(c, d) < target:
                            target = distance(c, d)
                            city = d
                visted.append(city)
                unvisted.remove(city)
                # print(visted)
                # print(unvisted)
                total += target
        return total

    def funcg(self):
        return self.cost

    def funcf(self):
        return self.funch() + self.funcg()
        # return 0 + self.funcg()

    def __lt__(self, other):
        return self.funcf() < other.funcf()

    def __cmp__(self, other):
        return self.visited == other.visted

    def __eq__(self, other):
        return self.__cmp__(other)

    def __hash__(self):
        return hash(str(self.visited))

    def __str__(self):
        return str(self.current)

def distance(x, y):
    return math.sqrt((x.x - y.x)**2 + (x.y - y.y)**2)

agent = TSP()
print(agent.getresult())