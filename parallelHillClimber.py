from solution import SOLUTION
from creature import CREATURE
import constants as c
import copy
import os
import numpy as np
import matplotlib.pyplot as plt
import time

class PARALLEL_HILL_CLIMBER:
    def __init__(self):

        #Deleting all preexisting temp files
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm body*.urdf")
        os.system("rm world*.sdf")

        self.initialParents = []

        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = CREATURE(self.nextAvailableID, i*1000)
            self.nextAvailableID += 1

        self.universalFitness = np.zeros((c.populationSize, c.numberOfGenerations+2))
        for index, parent in self.parents.items():
            self.universalFitness[index][0] = 0

    def Evolve(self):
        self.Evaluate(self.parents)
        for _, parent in self.parents.items():
            self.initialParents.append(parent)
        self.recordCurrentGenerationFitnesses(0)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
            self.recordCurrentGenerationFitnesses(currentGeneration+1)

    def recordCurrentGenerationFitnesses(self, currentGeneration):

        for index, parent in self.parents.items():
            self.universalFitness[index][currentGeneration+1] = parent.fitness * -1

    def saveFitnessPlot(self):
        for i in range(self.universalFitness.shape[0]):
            plt.plot(self.universalFitness[i], label='{}'.format(i+1))
        plt.xlabel("Number of generations")
        plt.ylabel("Fitness")
        plt.legend(loc='lower right',ncol=1, fancybox=True, shadow=True)
        plt.title("Fitnesses Of Evolving Robots")
        plt.savefig("Fitnessofevolvingrobot")


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
            self.children[id].currentGeneration += 1
            self.nextAvailableID += 1

    def Mutate(self):
        for _, child in self.children.items():
            child.Mutate()
        

    def Select(self):
        for id in self.parents.keys():
            if self.parents[id].fitness >= self.children[id].fitness:
                self.parents[id] = self.children[id]

    def Print(self):
        print("\n")
        for id, parent in self.parents.items():
            print("parent - ", parent.fitness, "child - ", self.children[id].fitness)

    def Show_Best(self):

        self.Show_Before_After()

        bestSolution = None
        for _, parent in self.parents.items():
            if not bestSolution:
                bestSolution = parent
            elif parent.fitness < bestSolution.fitness:
                bestSolution = parent

        bestSolution.Start_Simulation("GUI")

    def Show_Before_After(self):

        assert(len(self.initialParents) == c.populationSize)

        for parent in self.initialParents:
            parent.Start_Simulation("GUI")
            time.sleep(20)

        for parent in self.initialParents:
            parent.Wait_For_Simulation_To_End()

        all = self.parents.values()

        for parent in all:
            parent.Start_Simulation("GUI")
            time.sleep(20)

        for parent in all:
            parent.Wait_For_Simulation_To_End()


    def Evaluate(self, solutions):
        for _, solution in solutions.items():
                solution.Start_Simulation("DIRECT")
            
        for _, solution in solutions.items():
            solution.Wait_For_Simulation_To_End()


        