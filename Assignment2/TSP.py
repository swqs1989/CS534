import random as ra
from heapq import heappush, heapify, heappop
import numpy as np
import itertools
import math
import time

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "%r, %r" %(self.x, self.y)

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def add(self, item):
        heappush(self.queue, item)

    def remove(self, item):
        value = self.queue.remove(item)
        heapify(self.queue)
        return value is not None

    def peek(self):
        return self.queue[0]

    def poll(self):
        return heappop(self.queue)

    def __len__(self):
        return len(self.queue)

class TSP:
    def __init__(self, dictmap=None, city=None, visted=None, unvisted=None, cost=None, parent=None):
        # self.map = {0: City(12, 1), 1: City(2, 12), 2: City(89, 19), 3: City(77,24), 4: City(1, 11), 5: City(0, 9), 6: City(91, 79), 7: City(99, 43), 8: City(55, 49), 9: City(14, 99)} if dictmap is None else dictmap
        self.map = {0: City(23, 1), 1: City(7, 12), 2: City(8, 19), 3: City(99,24), 4: City(0, 84), 5: City(45, 9), 6: City(31, 42), 7: City(93,44), 8: City(9,99), 9: City(21,11), 10: City(67,12), 11: City(87,56), 12: City(33,44)} if dictmap is None else dictmap
        # self.map = {0: City(23, 1), 1: City(7, 12), 2: City(8, 19), 3: City(99,24), 4: City(0, 84), 5: City(45, 9), 6: City(31, 42), 7: City(93,44), 8: City(9,99)} if dictmap is None else dictmap
        self.current = city if city is not None else self.map[0]
        self.visited = visted if visted is not None else [self.map[0]]
        self.unvisted = unvisted if unvisted is not None else [self.map[i] for i in range(1, len(self.map))]
        self.cost = cost if cost is not None else 0
        self.parent = parent if parent is not None else None
        self.score = self.funcf()

    def gennextstep(self):
        for city in self.unvisted:
            visted = self.visited.copy()
            unvisted = self.unvisted.copy()
            visted.append(city)
            unvisted.remove(city)
            cost = self.cost + distance(self.current, city)
            yield TSP(self.map, city, visted, unvisted, cost, self)

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
                        if target is None:
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
        # print("mst: %r" %total)
        #return 0
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

class Agent:
    def __init__(self, initial=None):
        self.state = TSP(initial, None, None, None, None, None)

    def getPath(self, node):
        path = [node]
        state = node.parent
        while state.parent:
            path.append(state)
            state = state.parent
        return path

    def astar_program(self):
        queue = PriorityQueue()
        queue.add(self.state)
        explored = set()

        # print(self.state.cost)
        # print(self.state.current)

        while queue:
            node = queue.poll()

            if len(node.unvisted) == 0:
                path = self.getPath(node)
                truelength = distance(node.current, node.map[0]) + node.cost
                # print(node.cost)
                print("distance: %r" % node.cost)
                print("circle distance: %r" % truelength)
                # for state in path:
                    # print(state.funch())
                    # print(state.visited)
                    # print(state.current)
                break

            for state in node.gennextstep():
                if state not in explored:
                    queue.add(state)
            explored.add(node)


    def rbfs_program(self, node, flimit):
        if len(node.unvisted) == 0:
            truelength = distance(node.current, node.map[0]) + node.cost
            print("distance: %r" %node.cost)
            print("circle distance: %r" %truelength)
            path = self.getPath(node)
            # for state in path:
                # print(state.cost)
                # print(state.current)
            return node, flimit

        successors = []
        # print("00000000")
        for state in node.gennextstep():
            successors.append(state)
            # print(state.funch())
        # print("11111111")
        if len(successors) == 0:
            return None, 99999

        for s in successors:
            s.score = max(s.funcf(), node.score)

        while True:
            successors.sort(key=lambda x: x.score)
            best_succ = successors[0]
            if best_succ.score > flimit:
                node.score = best_succ.score

                return None, best_succ.score

            if len(successors) > 1:
                alter = successors[1].score
            else:
                alter = 99999

            result, bestf = self.rbfs_program(best_succ, min(flimit, alter))

            if result is not None:
                return result, bestf

class localagent:
    def __init__(self, initial=None):
        self.state = TSP(initial, None, None, None, None, None)
        self.currentpath = [i for i in range(1, len(self.state.map))]
        ra.shuffle(self.currentpath)
        # print(self.currentpath)
        self.matrix = None

    def genmatrix(self):
        self.matrix = np.array([[0 if i == j else distance(self.state.map[i], self.state.map[j]) for j in range(len(self.state.map))] for i in range(len(self.state.map))])

    def getdistance(self, i, j):
        return self.matrix[i][j]

    def hillclimbing(self, loops):
        tour = self.currentpath.copy()

        tot = self.getdistance(0, tour[0])
        for i in range(1, len(tour)):
            tot += self.getdistance(tour[i - 1], tour[i])
        tot += self.getdistance(tour[0], tour[len(tour) - 1])
        while loops > 0:

            cutpoint1 = ra.randint(0, len(tour) - 1)
            cutpoint2 = ra.randint(0, len(tour) - 1)
            while cutpoint1 == cutpoint2:
                cutpoint2 = ra.randint(0, len(tour) - 1)

            # print(cutpoint1)
            # print(cutpoint2)
            piece = [[],[],[]]
            for i in range(0, len(tour)):
                if i <= min(cutpoint1, cutpoint2):
                    piece[0].append(tour[i])
                elif i > min(cutpoint1, cutpoint2) and i < max(cutpoint1, cutpoint2):
                    piece[1].append(tour[i])
                else:
                    piece[2].append(tour[i])

            for perm in itertools.permutations(piece, 3):
                path = [item for list in perm for item in list]
                distance = self.getdistance(0, path[0])
                lastone = None
                for i in range(1, len(path)):
                    distance += self.getdistance(path[i-1], path[i])
                    lastone = path[i]

                distance += self.getdistance(0, lastone)
                if distance < tot:
                    tot = distance
                    tour = path
            loops -= 1

        print("circle distance: %r" %tot)
        return tour, tot

    def genetic(self, ngen=1000):
        population = self.random_selection()

        bestcost = 99999999999
        bestpath = None

        for i in range(ngen):
            random_selection = self.weighted_sample(population)

            x = random_selection[0]
            y = random_selection[1]

            child1, child2 = self.reproduce(x, y)

            x = random_selection[2]
            y = random_selection[3]

            child3, child4 = self.reproduce(x, y)

            population = [child1, child2, child3, child4]

            for child in population:
                self.mutate(child)
                if bestcost > self.getpathcost(child):
                    bestcost = self.getpathcost(child)
                    bestpath = child
        print("circle distance: %r" % bestcost)
        return bestpath, bestcost

    def mutate(self, path):
        seed1 = ra.randint(0, len(path) - 1)
        seed2 = ra.randint(0, len(path) - 1)
        while seed1 == seed2:
            seed2 = ra.randint(0, len(path) - 1)

        path[seed1], path[seed2] = path[seed2], path[seed1]

    def getpathcost(self, path):
        lodistance = self.getdistance(0, path[0])
        for i in range(1, len(path)):
            lodistance += self.getdistance(path[i - 1], path[i])

        lodistance += self.getdistance(0, path[len(path) - 1])
        return lodistance

    def fitness_func(self, path):
        lodistance = self.getdistance(0, path[0])
        for i in range(1, len(path)):
            lodistance += self.getdistance(path[i - 1], path[i])

        lodistance += self.getdistance(0, path[len(path) - 1])
        return 1/lodistance

    def reproduce(self, x, y):
        xx = x.copy()
        yy = y.copy()
        seed = ra.randint(2, len(x) - 2)
        change1 = xx[seed:]
        change2 = yy[seed:]

        diff2 = [i for i in change1 if i not in change2]
        difff2 = diff2.copy()
        diff1 = [i for i in change2 if i not in change1]
        difff1 = diff1.copy()
        for i in range(len(xx[:seed])):
            if xx[i] in difff1:
                xx[i] = diff2.pop()

        for i in range(len(yy[:seed])):
            if yy[i] in difff2:
                yy[i] = diff1.pop()

        xx = xx[:seed] + list(change2)
        yy = yy[:seed] + list(change1)

        return xx, yy

    def random_selection(self):
        """
        random generate 4 possible path, sorted according to the fitness_func
        :return: population
        """
        path = self.currentpath.copy()
        population = []
        fitness = []
        for i in range(4):
            ra.shuffle(path)
            population.append(path.copy())
            fitness.append(self.fitness_func(path.copy()))
        return self.weighted_sample(population)

    def weighted_sample(self, population, weight=None):
        """
        :param population: list -
        :param weight: list -
        :return: a sorted list based on the weight sample
        """
        # for i in range(len(population)):
        #     seed = ra.randint(0, len(pool))
        #     for p in pool:
        #         if seed >= p:
        #             return p
        population = sorted(population, key=lambda x: self.fitness_func(x))
        costlist = [self.fitness_func(p) for p in population]
        costlist = np.cumsum(costlist)
        result = []
        for i in range(4):
            seed = ra.randint(0, int(costlist[3] * 1000))
            pick = 0
            for j in range(len(costlist)):
                if seed > costlist[j] * 1000:
                    pick += 1
            result.append(population[pick])
        return result


def distance(x, y):
    return math.sqrt((x.x - y.x)**2 + (x.y - y.y)**2)

option = 1
# 0-tsp with A star and RBFS
# 1-tsp with hill climbing and genetic algorithm
if option == 0:
    astar = []
    rbfs = []
    hc = []
    ga = []

    for i in range(10):
        a = {}
        for i in range(15):
            c = City(ra.randint(0,1000), ra.randint(0,1000))
            a[i] = c

        # print(distance(a[1], a[2]))
        print("A*")

        agent1 = Agent(a)
        start = time.time()
        agent1.astar_program()
        end = time.time()
        astar.append(end - start)
        print("Total time used: %r" % (end - start))

        print("RBFS")

        agent2 = Agent(a)
        start = time.time()
        agent2.rbfs_program(agent2.state, 99999)

        end = time.time()
        rbfs.append(end - start)
        print("Total time used: %r" % (end - start))

    # print("Hill climbing")
    # la = localagent(a)
    # la.genmatrix()
    # start = time.time()
    # la.hillclimbing(100000)
    # end = time.time()
    # hc.append(end - start)
    # print("Total time used: %r" % (end - start))
    #
    # print("Genetic algorithm")
    # lga = localagent(a)
    # lga.genmatrix()
    # start = time.time()
    # lga.genetic(100000)
    # end = time.time()
    # ga.append(end - start)
    # print("Total time used: %r" % (end - start))
    # print("~" * 50)

    print(astar)
    print(rbfs)

if option == 1:
    astar = []
    hc = []

    for i in range(10):
        a = {}
        for i in range(13):
            c = City(ra.randint(0, 1000), ra.randint(0, 1000))
            a[i] = c

        # print(distance(a[1], a[2]))
        print("A*")

        agent1 = Agent(a)
        start = time.time()
        agent1.astar_program()
        end = time.time()
        astar.append(end - start)
        print("Total time used: %r" % (end - start))


        # print("RBFS")
        #
        # agent2 = Agent(a)
        # start = time.time()
        # agent2.rbfs_program(agent2.state, 99999)
        #
        # end = time.time()
        # rbfs.append(end - start)
        # print("Total time used: %r" % (end - start))

        print("Genetic algorithm with 1000")
        la = localagent(a)
        la.genmatrix()
        start = time.time()
        la.genetic(1000)
        end = time.time()
        hc.append(end - start)
        print("Total time used: %r" % (end - start))

        print("Genetic algorithm with 10000")
        la = localagent(a)
        la.genmatrix()
        start = time.time()
        la.genetic(10000)
        end = time.time()
        hc.append(end - start)
        print("Total time used: %r" % (end - start))

        print("Genetic algorithm with 100000")
        la = localagent(a)
        la.genmatrix()
        start = time.time()
        la.genetic()
        end = time.time()
        hc.append(end - start)
        print("Total time used: %r" % (end - start))
        print("*"*50)
        #
        # print("Genetic algorithm")
        # lga = localagent(a)
        # lga.genmatrix()
        # start = time.time()
        # lga.genetic(100000)
        # end = time.time()
        # ga.append(end - start)
        # print("Total time used: %r" % (end - start))
        # print("~" * 50)

    print(astar)
    print(hc)
#print(hc)
#print(ga)

# la = localagent()
# la.genmatrix()
#



# print(la.matrix[2][3])
# a = [0,1,2,3,4,5,6,7]
# for i in range(10):
#     print(ra.sample(range(1, 10), 9))
# for i in range(10):
#     ra.shuffle(a[1:])
#     print(a)

# for i in range(10):
#     print(ra.randint(1, 5))

# a = [1,2,3]
# b = [4,5,6]
# c = [7,8,9]
#
# d = [[],[],[]]
# d[0] = a
# d[1] = b
# d[2] = c
# for i in itertools.permutations(d, 3):
#     path = [item for l in i for item in l]
#     print(path)

# l = [1,2,3,4,5]
#
# ra.shuffle(l)
# print(l)
# l1 = []
# for i in range(10):
#     l1.append(ra.uniform(0, 1))
#     print(ra.randint(1, 5))
# l1 = [1/30, 1/40, 1/20, 1/10]
# print(np.cumsum(l1))
# print(sum(l1))
# for i in range(100):
#     print(ra.randint(1, 1000))

#    Local search performance
# la = localagent()
# la.genmatrix()
# a = [3,1,5,7,2,4,6]
# b = [7,1,6,4,3,2,5]
#
# print("========"*100)
# c, d = la.genetic(100000)
#
# print(c)
# print(d)
# print("="*100)
# tour, distance = la.hillclimbing(100000)
# print(tour)
# print(distance)