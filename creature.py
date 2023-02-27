import pyrosim.pyrosim as pyrosim
import os, time
import constants as c
import random
from creatureBody import CREATUREBODY
from cubeSide import CUBESIDE
from creationStats import CREATIONSTATS
from joint import JOINT

class CREATURE:
    def __init__(self, id):
        self.myId = id
        self.Generate_Random_Morphology()
        self.Preprocess_Generate_Body()

    def Generate_Random_Morphology(self):
        self.numberOfSections = random.randint(c.minimumSections, c.maximumSections)
        self.numberOfSensors = random.randint(self.numberOfSections//3, self.numberOfSections)
        self.sensorPositions = set(random.sample([i for i in range(self.numberOfSections)], self.numberOfSensors))
        self.creationStatistics = CREATIONSTATS()
        self.primaryParents = []
        self.joints = {}

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
        pyrosim.Start_SDF("world" + str(self.myId) + ".sdf")
        pyrosim.End()

    def Preprocess_Generate_Body(self):
        self.originLength = random.uniform(c.lowerBound, c.upperBound)
        self.originWidth = random.uniform(c.lowerBound, c.upperBound) 
        self.originHeight = random.uniform(c.lowerBound, c.upperBound)
        self.primarySections = set(random.sample([i+1 for i in range(6)], 3))

        if 1 in self.primarySections:
            self.joints[1] = JOINT(0, 1, [self.originLength/2, 0, 0.5], "0 0 1")
            self.primaryParents.append(CREATUREBODY(1, CUBESIDE.positiveLength, self.sensorPositions, self.creationStatistics))

        if 2 in self.primarySections:
            self.joints[2] = JOINT(0, 2, [-self.originLength/2, 0, 0.5], "0 0 1")
            self.primaryParents.append(CREATUREBODY(2, CUBESIDE.negativeLength, self.sensorPositions, self.creationStatistics))
        
        if 3 in self.primarySections:
            self.joints[3] = JOINT(0, 3, [0, self.originWidth/2, 0.5], "0 0 1")
            self.primaryParents.append(CREATUREBODY(3, CUBESIDE.positiveWidth, self.sensorPositions, self.creationStatistics))
        
        if 4 in self.primarySections:
            self.joints[4] = JOINT(0, 4, [0, -self.originWidth/2, 0.5], "0 0 1")
            self.primaryParents.append(CREATUREBODY(4, CUBESIDE.negativeWidth, self.sensorPositions, self.creationStatistics))
        
        if 5 in self.primarySections:
            self.joints[5] = JOINT(0, 5, [0, 0, 0.5+self.originHeight/2], "0 1 0")
            self.primaryParents.append(CREATUREBODY(5, CUBESIDE.positiveHeight, self.sensorPositions, self.creationStatistics))
        
        if 6 in self.primarySections:
            self.joints[6] = JOINT(0, 6, [0, 0, 0.5-self.originHeight/2], "0 1 0")
            self.primaryParents.append(CREATUREBODY(6, CUBESIDE.negativeHeight, self.sensorPositions, self.creationStatistics))


    def Generate_Body(self):
        pyrosim.Start_URDF("body" + str(self.myId) + ".urdf")
        pyrosim.Send_Cube(name=str(0), pos=[0, 0, 0.5], size=[self.originLength, self.originWidth, self.originHeight], c1='<material name="Cyan">',c2='    <color rgba="0 1.0 1.0 1.0"/>')

        for parent in self.primaryParents:
            parent.genBody()
            self.joints[parent.id].genJoint()

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







