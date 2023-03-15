from solution import SOLUTION
from creature import CREATURE
import constants as c
import copy
import os
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle

class PARALLEL_HILL_CLIMBER:
    def __init__(self, seed = 1):

        #Deleting all preexisting temp files
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm body*.urdf")
        os.system("rm world*.sdf")

        self.initialParents = []
        self.seed = seed

        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = CREATURE(self.nextAvailableID, (i+1)*seed)
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
        self.saveFitnessPlot()
        self.Save_Before_After()

    def recordCurrentGenerationFitnesses(self, currentGeneration):

        for index, parent in self.parents.items():
            self.universalFitness[index][currentGeneration+1] = parent.fitness * -1

    def saveFitnessPlot(self):
        for i in range(self.universalFitness.shape[0]):
            plt.plot(self.universalFitness[i], label='{}'.format(i+1))
        plt.xlabel("Number of generations")
        plt.ylabel("Fitness")
        plt.legend(loc='lower right',ncol=1, fancybox=True, shadow=True)
        plt.title("Fitnesses Of Evolving Robots with Seed = {}".format(self.seed))
        plt.savefig("{}FitnessOfEvolvingRobotWithSeed{}.png".format(c.fitnessGraphFilePath, self.seed))
        plt.close()
        self.Save(self.universalFitness, "{}universalFitness{}.p".format(c.fitnessFilePath, self.seed))



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

    def Get_Best(self):

        bestSolution = None
        for _, parent in self.parents.items():
            if not bestSolution:
                bestSolution = parent
            elif parent.fitness < bestSolution.fitness:
                bestSolution = parent
        return bestSolution

    def Save_Before_After(self):

        assert(len(self.initialParents) == c.populationSize)
        for index, parent in enumerate(self.initialParents):
            self.Save(parent, "{}seed_{}_initial_parent_{}.p".format(c.initialParentsFilePath, self.seed, index))

        all = self.parents.values()

        for index, parent in enumerate(all):
            self.Save(parent, "{}seed_{}_final_state_{}.p".format(c.finalParentsFilePath, self.seed, index))

        self.Save(self.Get_Best(), "{}seed_{}_best_state.p".format(c.bestStateFilePath, self.seed))



    def Save(self, parent, filename):

        with open(filename, 'wb') as output:
            pickle.dump(parent, output, pickle.HIGHEST_PROTOCOL)
        output.close()

    def Evaluate(self, solutions):
        for _, solution in solutions.items():
                solution.Start_Simulation("DIRECT")
            
        for _, solution in solutions.items():
            solution.Wait_For_Simulation_To_End()


        