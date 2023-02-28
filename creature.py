import pyrosim.pyrosim as pyrosim
import os, time
import constants as c
import random
from creatureBody import CREATUREBODY
from cubeSide import CUBESIDE
from creationStats import CREATIONSTATS
from joint import JOINT
import numpy as np

class CREATURE:
    def __init__(self, id, seed=time.time()):
        self.myId = id
        random.seed(seed)
        self.Generate_Random_Morphology()
        self.Preprocess_Generate_Body()
        self.currentGeneration = 0

    def Generate_Random_Morphology(self):
        self.numberOfSections = random.randint(c.minimumSections, c.maximumSections)
        self.numberOfSensors = random.randint(17*self.numberOfSections//20, self.numberOfSections)
        self.sensorPositions = set(random.sample([i for i in range(self.numberOfSections)], self.numberOfSensors))
        self.addedSecondarySections = []
        self.addedTertiarySections = []
        self.originLength = random.uniform(c.lowerBound, c.upperBound)
        self.originWidth = random.uniform(c.lowerBound, c.upperBound) 
        self.originHeight = random.uniform(c.lowerBound, c.upperBound)
        self.numPrimarySections = random.randint(3, 5)

        #Take another look at weights later
        self.weights = np.random.rand(self.numberOfSections, self.numberOfSections)
        self.weights = self.weights * 2 - 1
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
        os.system("rm brain" + str(self.myId) + ".nndf")
        os.system("rm world" + str(self.myId) + ".sdf")

    def Create_World(self):
        pyrosim.Start_SDF("world" + str(self.myId) + ".sdf")
        pyrosim.End()

    def Preprocess_Generate_Body(self):
        self.primarySections = set(random.sample([i+1 for i in range(6)], self.numPrimarySections))
        self.primaryParents = []
        self.creationStatistics = CREATIONSTATS()
        self.creationStatistics.sensors.append(0)

        if 1 in self.primarySections:
            self.joints[1] = JOINT(0, 1, [self.originLength/2, 0, 0.5], "0 0 1", self.creationStatistics)
            self.primaryParents.append(CREATUREBODY(1, CUBESIDE.positiveLength, self.sensorPositions, self.creationStatistics))

        if 2 in self.primarySections:
            self.joints[2] = JOINT(0, 2, [-self.originLength/2, 0, 0.5], "0 0 1", self.creationStatistics)
            self.primaryParents.append(CREATUREBODY(2, CUBESIDE.negativeLength, self.sensorPositions, self.creationStatistics))
        
        if 3 in self.primarySections:
            self.joints[3] = JOINT(0, 3, [0, self.originWidth/2, 0.5], "0 0 1", self.creationStatistics)
            self.primaryParents.append(CREATUREBODY(3, CUBESIDE.positiveWidth, self.sensorPositions, self.creationStatistics))
        
        if 4 in self.primarySections:
            self.joints[4] = JOINT(0, 4, [0, -self.originWidth/2, 0.5], "0 0 1", self.creationStatistics)
            self.primaryParents.append(CREATUREBODY(4, CUBESIDE.negativeWidth, self.sensorPositions, self.creationStatistics))
        
        if 5 in self.primarySections:
            self.joints[5] = JOINT(0, 5, [0, 0, 0.5+self.originHeight/2], "0 1 0", self.creationStatistics)
            self.primaryParents.append(CREATUREBODY(5, CUBESIDE.positiveHeight, self.sensorPositions, self.creationStatistics))
        
        if 6 in self.primarySections:
            self.joints[6] = JOINT(0, 6, [0, 0, 0.5-self.originHeight/2], "0 1 0", self.creationStatistics)
            self.primaryParents.append(CREATUREBODY(6, CUBESIDE.negativeHeight, self.sensorPositions, self.creationStatistics))


    def Generate_Body(self):
        pyrosim.Start_URDF("body" + str(self.myId) + ".urdf")
        pyrosim.Send_Cube(name=str(0), pos=[0, 0, 0.5], size=[self.originLength, self.originWidth, self.originHeight], c1='<material name="Cyan">',c2='    <color rgba="0 1.0 1.0 1.0"/>')

        for parent in self.primaryParents:
            parent.genBody()
            self.joints[parent.id].genJoint()

        for parent in self.addedSecondarySections:
            parent.genBody()
            self.joints[parent.id].genJoint()

        for parent in self.addedTertiarySections:
            parent.genBody()
            self.joints[parent.id].genJoint()

        pyrosim.End() 

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myId) + ".nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName =str(0))

        for cube in self.primaryParents:
            cube.generateBrain()
            self.joints[cube.id].genBrain()

        for cube in self.addedSecondarySections:
            cube.generateBrain()
            self.joints[cube.id].genBrain()

        for cube in self.addedTertiarySections:
            cube.generateBrain()
            self.joints[cube.id].genBrain()

        for sensor in self.creationStatistics.sensors:
            for motor in self.creationStatistics.motorId:
                pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor,  weight = self.weights[sensor][motor-c.offsetForMotors])
        pyrosim.End()

    def Mutate(self):

        if self.currentGeneration%15 == 0:
            assert(len(self.addedSecondarySections) == 0)
            assert(len(self.addedTertiarySections) ==  0)
            self.Preprocess_Generate_Body()

        elif self.currentGeneration%15 == 2:
            assert(len(self.addedSecondarySections) == 0)
            assert(len(self.addedTertiarySections) ==  0)
            pickedParent = self.primaryParents[random.randint(0, self.numPrimarySections-1)]
            side = self.randomSideExcept(pickedParent.connectorFace)
            self.addedSecondarySections.append(CREATUREBODY(7, side, self.sensorPositions, self.creationStatistics))
            jointDim, jointRev = JOINT.generateJointDimensions(pickedParent, side)
            self.joints[7] = JOINT(pickedParent.id, 7, jointDim, jointRev, self.creationStatistics)

        elif self.currentGeneration%15 == 4:
            assert(len(self.addedSecondarySections) == 1)
            assert(len(self.addedTertiarySections) ==  0)
            pickedParent = self.primaryParents[random.randint(0, self.numPrimarySections-1)]
            while(pickedParent.id == self.joints[7].parent):
                pickedParent = self.primaryParents[random.randint(0, self.numPrimarySections-1)]
            side = self.randomSideExcept(pickedParent.connectorFace)
            self.addedSecondarySections.append(CREATUREBODY(8, side, self.sensorPositions, self.creationStatistics))
            jointDim, jointRev = JOINT.generateJointDimensions(pickedParent, side)
            self.joints[8] = JOINT(pickedParent.id, 8, jointDim, jointRev, self.creationStatistics)

        elif self.currentGeneration%15 == 6:
            assert(len(self.addedSecondarySections) == 2)
            assert(len(self.addedTertiarySections) ==  0)
            pickedParent = self.addedSecondarySections[0]
            side = self.randomSideExcept(pickedParent.connectorFace)
            self.addedTertiarySections.append(CREATUREBODY(9, side, self.sensorPositions, self.creationStatistics))
            jointDim, jointRev = JOINT.generateJointDimensions(pickedParent, side)
            self.joints[9] = JOINT(pickedParent.id, 9, jointDim, jointRev, self.creationStatistics)

        elif self.currentGeneration%15 == 8:
            assert(len(self.addedSecondarySections) == 2)
            assert(len(self.addedTertiarySections) ==  1)
            pickedParent = self.addedSecondarySections[1]
            side = self.randomSideExcept(pickedParent.connectorFace)
            self.addedTertiarySections.append(CREATUREBODY(10, side, self.sensorPositions, self.creationStatistics))
            jointDim, jointRev = JOINT.generateJointDimensions(pickedParent, side)
            self.joints[10] = JOINT(pickedParent.id, 10, jointDim, jointRev, self.creationStatistics)

        elif self.currentGeneration%15 == 10:
            assert(len(self.addedSecondarySections) == 2)
            assert(len(self.addedTertiarySections) ==  2)
            self.addedSecondarySections.pop(0)
            self.addedTertiarySections.pop(0)
            self.creationStatistics.motorId.remove(self.joints[7].motorId)
            self.creationStatistics.motorId.remove(self.joints[9].motorId)
            if 7 in self.creationStatistics.sensors:
                self.creationStatistics.sensors.remove(7) 
            if 9 in self.creationStatistics.sensors:
                self.creationStatistics.sensors.remove(9) 

        elif self.currentGeneration%15 == 12:
            assert(len(self.addedSecondarySections) == 1)
            assert(len(self.addedTertiarySections) ==  1)
            self.addedTertiarySections.pop()
            self.creationStatistics.motorId.remove(self.joints[10].motorId)
            if 10 in self.creationStatistics.sensors:
                self.creationStatistics.sensors.remove(10)

        elif self.currentGeneration%15 == 14:
            assert(len(self.addedSecondarySections) == 1)
            assert(len(self.addedTertiarySections) ==  1)
            self.addedSecondarySections.pop()
            self.creationStatistics.motorId.remove(self.joints[8].motorId)
            if 8 in self.creationStatistics.sensors:
                self.creationStatistics.sensors.remove(8)

        else:
            indexRow = np.random.randint(0, 5)
            indexColumn = np.random.randint(0, 5)
            self.weights[indexRow][indexColumn] = np.random.random() * 2 -1

            
        
    def randomSideExcept(self, side):
        chosenSide = random.choice([CUBESIDE(i+1) for i in range(6)])

        while (side == chosenSide):
            chosenSide = random.choice([CUBESIDE(i+1) for i in range(6)])

        return chosenSide

    

        #Mutation strategies
        #0. Evolve all primaries
        #3. Add a body part to primary (p1)
        #6. Add another body part to primary (p2)
        #9. Add a body part to secondary (p1->p3)
        #12. Add another body part to secondary (p2->p4)
        #15. Remove both (p1 and p1-> p2)
        #18. Remove p2->p4
        #21. Remove p2
        #22 - 24. Evolve brain only

        

    def Set_ID(self, id):
        self.myId = id







