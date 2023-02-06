import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os

from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self, solutionId):

        self.solutionId = solutionId
        self.robotId = p.loadURDF("body" + str(self.solutionId)+ ".urdf")
        self.motor = {}
        self.sensor = {}
        self.nn = NEURAL_NETWORK("brain" + str(self.solutionId) + ".nndf")

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        os.system("rm brain" + str(self.solutionId) + ".nndf")

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensor[linkName] = SENSOR(linkName)

    def sense(self, index):
        for linkName in self.sensor.keys():
            self.sensor[linkName].Get_Value(index)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motor[jointName] = MOTOR(jointName)

    def Act(self, index):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointChange
                self.motor[jointName].Set_Value(desiredAngle, self)

    def Think(self):
        self.nn.Update()
        self.nn.Print()

    def Get_Fitness(self):
        # basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        # basePosition = basePositionAndOrientation[0]
        # xPosition = basePosition[0]
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]


        f = open("tmp" + str(self.solutionId) + ".txt", "w")
        f.write(str(positionOfLinkZero[0]))
        f.close()

        os.system("mv tmp" + str(self.solutionId) + ".txt fitness" + str(self.solutionId) + ".txt")

         






