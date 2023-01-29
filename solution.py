from generate import Create_World
import numpy as np
import pyrosim.pyrosim as pyrosim
import os

class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3,2)
        self.weights = self.weights * 2 - 1

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("python3 simulate.py "+ directOrGUI)

        f = open("fitness.txt", "r")
        self.fitness = float(f.read())
        f.close()

    def Create_World(self):
        x, y, z = -2, 2, 0.1
        length, width, height = 1, 1, 1
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_Backleg", parent= "Torso",child = "Backleg" ,type = "revolute", position = [-0.5,0,1.0])
        pyrosim.Send_Cube(name="Backleg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_Frontleg", parent= "Torso",child = "Frontleg" ,type = "revolute", position = [0.5,0,1.0])
        pyrosim.Send_Cube(name="Frontleg", pos=[0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Backleg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Frontleg")

        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_Backleg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_Frontleg")

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn+3,
                        weight = self.weights[currentRow][currentColumn])
    
        pyrosim.End()

    def Mutate(self):
        indexRow = np.random.randint(0, 2)
        indexColumn = np.random.randint(0, 1)

        self.weights[indexRow][indexColumn] = np.random.random() * 2 -1




