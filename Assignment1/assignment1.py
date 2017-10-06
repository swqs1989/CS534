import random as ra
# Environment is the real environment that records the whole information
class Environment:
    def __init__(self, d=None, agent=None):
        self.squares = d if d is not None else {"A": "Clean", "B": "Clean"}
        self.score = 0
        #self.agent = agent

    # for each iteration, the environment changes its state by chance

    def performance(self):
        for location, status in self.squares.items():
            if status == "Clean":
                self.score += 1

        return self.score

    # randomly generate dirty
    def generateDirty(self):
        # each square 20% chance to be dirty
        # if it is already dirty, then it stays dirty
        rand1, rand2 = ra.randint(0, 4), ra.randint(0, 4)
        if rand1 == 0 and self.squares["A"] == "Clean":
            self.squares["A"] = "Dirty"
        if rand2 == 0 and self.squares["B"] == "Clean":
            self.squares["B"] = "Dirty"

# agent of vacuum
class VacuumAgent:
    def __init__(self, env, loc=None):
        self.location = ("A" if ra.randint(0, 1) == 0 else "B") if loc is None else loc
        self.status = ""
        self.percept(env)
        self.actionlist = []

    # percept the environment and act accordingly
    def program(self, env):
        self.percept(env)
        return self.act(env)

    def percept(self, env):
        self.status = env.squares[self.location]
        return 0

    def act(self, env):
        if self.status == "Dirty":
            env.squares[self.location] = "Clean"
            self.actionlist.append("Suck")
            return "Suck"
        elif self.location == "A":
            self.location = "B"
            self.actionlist.append("Right")
            return "Right"
        else:
            self.location = "A"
            self.actionlist.append("Left")
            return "Left"


initialLoc = ["A", "B"]
initialState = ["Clean", "Dirty"]

initialEnv = [{"A": "Clean", "B": "Clean"},{"A": "Dirty", "B": "Clean"},{"A": "Clean", "B": "Dirty"},{"A": "Dirty", "B": "Dirty"}]

file = open("output.txt", "w+")

for ienv in initialEnv:
    for agentloc in initialLoc:
        print("Environment: %r, Agent Location: %r" % (ienv, agentloc))
        file.write("Environment: %r, Agent Location: %r \n" % (ienv, agentloc))
        env = Environment(ienv.copy())
        va = VacuumAgent(env, agentloc)
        for i in range(1000):
            # env.generateDirty()
            env.performance()
            va.program(env)
        print(env.score)
        file.write("The score is %r \n" %env.score)
        for action in va.actionlist:
            file.write("%r \n" %action)
