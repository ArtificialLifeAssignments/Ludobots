from solution import SOLUTION

class HILL_CLIMBER:
    def __init__(self):

        self.parent = SOLUTION()
        pass

    def Evolve(self):
        self.parent.Evaluate()