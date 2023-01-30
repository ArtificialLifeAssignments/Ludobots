from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):

        #Deleting all preexisting temp files
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")


        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        for _, parent in self.parents.items():
            parent.Start_Simulation("DIRECT")
            
        for _, parent in self.parents.items():
            parent.Wait_For_Simulation_To_End()
        

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()


    def Evolve_For_One_Generation(self):
        # self.Spawn()
        # self.Mutate()
        # self.child.Evaluate("DIRECT")
        # self.Print()
        # self.Select()
        pass

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        self.child.Set_ID(self.nextAvailableID)
        self.nextAvailableID += 1

    def Mutate(self):
        self.child.Mutate()
        

    def Select(self):
        if self.parent.fitness >= self.child.fitness:
            self.parent = self.child

    def Print(self):
        # f = open("fitnesses.txt", "a")
        # f.write("parent - " + str(self.parent.fitness)+ " child - " + str(self.child.fitness))
        # f.close()
        print("parent - ", self.parent.fitness, "child - ", self.child.fitness)

    def Show_Best(self):
        # self.parent.Evaluate("GUI")
        pass
        