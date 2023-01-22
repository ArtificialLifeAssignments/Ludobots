import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c

from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self):

        self.robotId = p.loadURDF("body.urdf")
        self.motor = {}
        self.sensor = {}

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

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
        for jointName in self.motor.keys():
            self.motor[jointName].Set_Value(index, self)







