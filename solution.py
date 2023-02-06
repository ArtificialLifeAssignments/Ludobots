import numpy as np
import pyrosim.pyrosim as pyrosim
import os, time
import constants as c

class SOLUTION:
    def __init__(self, id):
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        self.myId = id


    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myId) +  " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myId) + ".txt"

        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        f = open(fitnessFileName, "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm " + fitnessFileName)
        os.system("rm body" + str(self.myId) + ".urdf")
        os.system("rm world" + str(self.myId) + ".sdf")

    def Create_World(self):
        x, y, z = -2, 2, 0.1
        length, width, height = 1, 1, 1
        pyrosim.Start_SDF("world" + str(self.myId) + ".sdf")
        pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body" + str(self.myId) + ".urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_Backleg", parent= "Torso",child = "Backleg",
                type = "revolute", position = [0, -0.5, 1], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name="Backleg", pos=[0, -0.5, 0], size=[0.2, 1.0, 0.2])
        pyrosim.Send_Joint(name="Torso_Frontleg", parent= "Torso",child = "Frontleg",
                type = "revolute", position = [0,0.5,1.0], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name="Frontleg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name="Torso_Leftleg", parent= "Torso",child = "Leftleg",
                type = "revolute", position = [-0.5, 0, 1], jointAxis= "0 1 0")
        pyrosim.Send_Cube(name="Leftleg", pos=[-0.5, 0, 0], size=[1.0, 0.2, 0.2])
        pyrosim.Send_Joint(name="Torso_Rightleg", parent= "Torso",child = "Rightleg",
                type = "revolute", position = [0.5, 0, 1], jointAxis= "0 1 0")
        pyrosim.Send_Cube(name="Rightleg", pos=[0.5, 0, 0], size=[1.0, 0.2, 0.2])
      

        pyrosim.Send_Joint(name="Frontleg_Frontlowerleg", parent= "Frontleg",child = "Frontlowerleg",
                type = "revolute", position = [0, 1, 0], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name="Frontlowerleg", pos=[0, 0.1, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="Backleg_Backlowerleg", parent= "Backleg",child = "Backlowerleg",
                type = "revolute", position = [0, -1, 0], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name="Backlowerleg", pos=[0, -0.1, -0.5], size=[0.2, 0.2, 1])


        pyrosim.Send_Joint(name="Leftleg_Leftlowerleg", parent= "Leftleg",child = "Leftlowerleg",
                type = "revolute", position = [-1, 0, 0], jointAxis= "0 1 0")
        pyrosim.Send_Cube(name="Leftlowerleg", pos=[-0.1, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="Rightleg_Rightlowerleg", parent= "Rightleg",child = "Rightlowerleg",
                type = "revolute", position = [1, 0, 0], jointAxis= "0 1 0")
        pyrosim.Send_Cube(name="Rightlowerleg", pos=[0.1, 0, -0.5], size=[0.2, 0.2, 1])
        




        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myId) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Backleg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Frontleg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "Leftleg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "Rightleg")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "Frontlowerleg")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "Backlowerleg")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "Leftlowerleg")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "Rightlowerleg")


        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_Backleg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_Frontleg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "Torso_Leftleg")
        pyrosim.Send_Motor_Neuron( name = 12 , jointName = "Torso_Rightleg")
        pyrosim.Send_Motor_Neuron( name = 13 , jointName ="Frontleg_Frontlowerleg")
        pyrosim.Send_Motor_Neuron( name = 14 , jointName ="Backleg_Backlowerleg")
        pyrosim.Send_Motor_Neuron( name = 15 , jointName ="Leftleg_Leftlowerleg")
        pyrosim.Send_Motor_Neuron( name = 16 , jointName ="Rightleg_Rightlowerleg")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn+c.numSensorNeurons,
                        weight = self.weights[currentRow][currentColumn])
    
        pyrosim.End()

    def Mutate(self):
        indexRow = np.random.randint(0, c.numSensorNeurons-1)
        indexColumn = np.random.randint(0, c.numMotorNeurons-1)

        self.weights[indexRow][indexColumn] = np.random.random() * 2 -1

    def Set_ID(self, id):
        self.myId = id




