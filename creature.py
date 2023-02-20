import pyrosim.pyrosim as pyrosim
import os, time
import constants as c
import random
from creatureBody import CREATUREBODY
from cubeSide import CUBESIDE
from creationStats import CREATIONSTATS

class CREATURE:
    def __init__(self, id, seed=1676127262.929452):
        self.myId = id
        # random.seed(time.time)
        self.seed = seed

    def Generate_Random_Morphology(self):
        self.numberOfSections = random.randint(c.minimumSections, c.maximumSections)
        self.numberOfSensors = random.randint(self.numberOfSections//3, self.numberOfSections)
        self.sensorPositions = set(random.sample([i for i in range(self.numberOfSections)], self.numberOfSensors))
        self.numberOfDescendants = random.randint(self.numberOfSections//3, self.numberOfSections)
        self.canHaveKids = set(random.sample([i for i in range(self.numberOfSections)], self.numberOfDescendants))

        self.creationStatistics = CREATIONSTATS()
        self.primaryParents = []

    def Start_Simulation(self, directOrGUI):
        self.Generate_Random_Morphology()
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
        pyrosim.Start_SDF("world" + str(self.myId) + ".sdf")
        pyrosim.End()

    def Generate_Body(self):
        length = random.uniform(c.lowerBound, c.upperBound)
        width = random.uniform(c.lowerBound, c.upperBound) 
        height = random.uniform(c.lowerBound, c.upperBound)
        self.primarySections = set(random.sample([i+1 for i in range(6)], 3))
        
        pyrosim.Start_URDF("body" + str(self.myId) + ".urdf")

        pyrosim.Send_Cube(name=str(0), pos=[0, 0, 0.5], size=[length, width, height], c1='<material name="Cyan">',c2='    <color rgba="0 1.0 1.0 1.0"/>')

        if 1 in self.primarySections:
            pyrosim.Send_Joint(name="0_1", parent=str(0), child=str(1),
                     type = "revolute", position = [length/2, 0, 0.5], jointAxis= "0 0 1")
            self.primaryParents.append(CREATUREBODY(1, 0, 0, CUBESIDE.positiveLength, self.sensorPositions, self.canHaveKids, self.creationStatistics))

        if 2 in self.primarySections:
            pyrosim.Send_Joint(name="0_2", parent=str(0), child=str(2),
                     type = "revolute", position = [-length/2, 0, 0.5], jointAxis= "0 0 1")
            self.primaryParents.append(CREATUREBODY(2, 0, 0, CUBESIDE.negativeLength, self.sensorPositions, self.canHaveKids, self.creationStatistics))
        
        if 3 in self.primarySections:
            pyrosim.Send_Joint(name="0_3", parent=str(0), child=str(3),
                     type = "revolute", position = [0, width/2, 0.5], jointAxis= "0 0 1")
            self.primaryParents.append(CREATUREBODY(3, 0, 0, CUBESIDE.positiveWidth, self.sensorPositions, self.canHaveKids, self.creationStatistics))
        
        if 4 in self.primarySections:
            pyrosim.Send_Joint(name="0_4", parent=str(0), child=str(4),
                     type = "revolute", position = [0, -width/2, 0.5], jointAxis= "0 0 1")
            self.primaryParents.append(CREATUREBODY(4, 0, 0, CUBESIDE.negativeWidth, self.sensorPositions, self.canHaveKids, self.creationStatistics))
        
        if 5 in self.primarySections:
            pyrosim.Send_Joint(name="0_5", parent=str(0), child=str(5),
                     type = "revolute", position = [0, 0, 0.5+height/2], jointAxis= "0 1 0")
            self.primaryParents.append(CREATUREBODY(5, 0, 0, CUBESIDE.positiveHeight, self.sensorPositions, self.canHaveKids, self.creationStatistics))
        
        if 6 in self.primarySections:
            pyrosim.Send_Joint(name="0_6", parent=str(0), child=str(6),
                     type = "revolute", position = [0, 0, 0.5-height/2], jointAxis= "0 1 0")
            self.primaryParents.append(CREATUREBODY(6, 0, 0, CUBESIDE.negativeHeight, self.sensorPositions, self.canHaveKids, self.creationStatistics))
                    
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myId) + ".nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName =str(0))
        self.creationStatistics.sensors.append(0)

        for cube in self.primaryParents:
            cube.generateBrain()

        for sensor in self.creationStatistics.sensors:
            for motor in self.creationStatistics.motorId:
                pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight = random.random() * 2 -1)
        pyrosim.End()

    def Mutate(self):
        pass

    def Set_ID(self, id):
        self.myId = id







