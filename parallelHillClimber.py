from solution import SOLUTION
from snake import SNAKE
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):

        #Deleting all preexisting temp files
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm body*.urdf")
        os.system("rm world*.sdf")


        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SNAKE(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()


    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for id, parent in self.parents.items():
            self.children[id] = copy.deepcopy(parent)
            self.children[id].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for _, child in self.children.items():
            child.Mutate()
        

    def Select(self):
        for id in self.parents.keys():
            if self.parents[id].fitness > self.children[id].fitness:
                self.parents[id] = self.children[id]

    def Print(self):
        print("\n")
        for id, parent in self.parents.items():
            print("parent - ", parent.fitness, "child - ", self.children[id].fitness)

    def Show_Best(self):
        bestSolution = None
        for _, parent in self.parents.items():
            if not bestSolution:
                bestSolution = parent
            elif parent.fitness < bestSolution.fitness:
                bestSolution = parent

        bestSolution.Start_Simulation("GUI")

    def Evaluate(self, solutions):
        for _, solution in solutions.items():
                solution.Start_Simulation("DIRECT")
            
        for _, solution in solutions.items():
            solution.Wait_For_Simulation_To_End()


        