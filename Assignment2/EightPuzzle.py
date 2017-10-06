from heapq import heappush, heapify, heappop
import numpy as np
import time
import random as ra

class Board:
    def __init__(self, setup, count=0, parent=None):
        self.setup = setup
        self.count = count
        self.parent = parent
        self.score = self.funcf()
        self.goal = [i for i in range(9)]

    def gennextstep(self, count):
        """
        this function is to get a generator for successors of a state
        :param count:
        :return:
        """
        blank = self.setup.index(0)

        # for those the blank can move down
        if blank in [0,1,2,3,4,5]:
            new_setup = self.setup.copy()
            new_setup[blank], new_setup[blank + 3] = new_setup[blank + 3], new_setup[blank]
            yield Board(new_setup, count, self)

        if blank in [3,4,5,6,7,8]:
            new_setup = self.setup.copy()
            new_setup[blank], new_setup[blank - 3] = new_setup[blank - 3], new_setup[blank]
            yield Board(new_setup, count, self)

        if blank in [0,1,3,4,6,7]:
            new_setup = self.setup.copy()
            new_setup[blank], new_setup[blank + 1] = new_setup[blank + 1], new_setup[blank]
            yield Board(new_setup, count, self)

        if blank in [1,2,4,5,7,8]:
            new_setup = self.setup.copy()
            new_setup[blank], new_setup[blank - 1] = new_setup[blank - 1], new_setup[blank]
            yield Board(new_setup, count, self)

    def funcg(self):
        return self.count

    def funch(self):
        return self.calManhattanDist() + ra.randint(0, 2)

    def calManhattanDist(self):
        total = 0
        for i in range(1, 9):
            pos = self.setup.index(i)
            # vertical distance
            dis = pos // 3 - i // 3 if pos > i else i // 3 - pos // 3
            # horizontal distance
            dis += (pos % 3 - i % 3) if pos % 3 > i % 3 else (i % 3 - pos % 3)
            total += dis
        return total

    def funcf(self):
        return self.funcg() + self.funch()

    def __lt__(self, other):
        return self.funcf() < other.funcf()

    def __cmp__(self, other):
        return self.setup == other.setup

    def __eq__(self, other):
        return self.__cmp__(other)

    def __hash__(self):
        return hash(str(self.setup))

    def __str__(self):
        return str(self.setup)

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

class Agent:
    def __init__(self, initial):
        self.state = Board(initial)
        self.goal = [i for i in range(9)]

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
        count = 0
        while queue:
            # print(queue.__len__())
            # print(explored.__len__())
            node = queue.poll()
            if node.setup == self.goal:
                # print(node.count)
                path = self.getPath(node)
                for state in path:
                    print(state)
                break

            count += 1
            # print(node)
            for state in node.gennextstep(count):
                if state not in explored:
                    queue.add(state)
            explored.add(node)

    def rbfs_program(self, node, flimit, count):
        # print(node.setup)
        if node.setup == self.goal:
            path = self.getPath(node)
            for state in path:
                print(state)
            return node, flimit

        successors = []
        count += 1
        for state in node.gennextstep(count):
            successors.append(state)

        if len(successors) == 0:
            return None, 999

        for s in successors:
            s.score = max(s.funcf(), node.score)

        while True:
            successors.sort(key=lambda x: x.score)
            # for s in successors:
            #     print(s.score)
            # print("=" * 30)
            best_succ = successors[0]
            if best_succ.score > flimit:
                node.score = best_succ.score
                # print(best_succ.score)
                return None, best_succ.score
            if len(successors) > 1:
                alter = successors[1].score
            else:
                alter = 999
            result, bestf = self.rbfs_program(best_succ, min(flimit, alter), count)
            if result is not None:
                return result, bestf





# b = Board([8,1,2,3,4,5,6,7,0], 1, None)
# print(b.calManhattanDist())

# explored = set()
# explored.add(Board([7,2,4,5,0,6,8,3,1]))
#
# b1 = Board([7,2,4,5,0,6,8,3,1])
#
# i = 1
# while i < 4:
#     for state in b1.gennextstep(0):
#         if state not in explored:
#             print(state)
#             explored.add(state)
#     i += 1
#
#
# print("explored")
# for a in explored:
#     print(a)
test = [4,1,3,0,5,8,7,2,6]
def checkstate(array):
    total = 0
    for i in range(len(array)):
        for j in range(i+1, len(array)):
            if array[i] > array[j] and array[i] != 0 and array[j] != 0:
                total += 1
    return total % 2 == 0
print(checkstate(test))
# print(checkstate([7,2,4,5,0,6,8,3,1]))

# agent = Agent([1,2,0,3,4,5,6,7,8])
# agent = Agent([1,2,3,4,0,5,6,7,8])
# agent = Agent([1,2,3,4,0,5,6,7,8])
# agent = Agent([7,2,4,5,0,6,8,3,1])
# print(agent.program())
# [5, 6, 4, 2, 0, 1, 7, 3, 8]
# [2, 1, 5, 3, 4, 0, 6, 7, 8]


agent = Agent([4,1,3,0,5,8,7,2,6])
# agent.astar_program()
start = time.time()
agent.rbfs_program(agent.state,999, 0)
end = time.time()
print("Total time used: %r" %(end - start))

# sample = np.random.choice(9, 9, replace=False)
# print(sample)
#
# agent = Agent(sample.tolist())
# agent.rbfs_program(agent.state,999, 0)

# astar = []
# rbfs = []
#
# for i in range(10):
#     sample = np.random.choice(9, 9, replace=False).tolist()
#     while not checkstate(sample):
#         sample = np.random.choice(9, 9, replace=False).tolist()
#     print(sample)
#
#     print("A*")
#     start = time.time()
#     agent = Agent(sample)
#     agent.astar_program()
#     end = time.time()
#     astar.append(end - start)
#     print("Total time used: %r" %(end - start))
#
#     print("RBFS")
#     start = time.time()
#     agent = Agent(sample)
#     agent.rbfs_program(agent.state, 999, 0)
#     end = time.time()
#     rbfs.append(end - start)
#     print("Total time used: %r" % (end - start))
#
#     print("~"*50)
#
# print(astar)
# print(rbfs)
