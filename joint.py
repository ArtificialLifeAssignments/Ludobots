import pyrosim.pyrosim as pyrosim
from cubeSide import CUBESIDE
import constants as c

class JOINT:
    def __init__(self, parent, child, position, jointAxis, creationStatistics):
        self.parent = str(parent)
        self.child = str(child)
        self.position = position
        self.jointAxis = jointAxis
        self.creationStatistics = creationStatistics
        self.motorId = int(self.child) + c.offsetForMotors
        self.creationStatistics.motorId.append(self.motorId)

    def genJoint(self):
        pyrosim.Send_Joint(name=self.parent+"_"+self.child, parent=self.parent, child=self.child,
                     type = "revolute", position = self.position, jointAxis= self.jointAxis)
        

    def genBrain(self):
        pyrosim.Send_Motor_Neuron(name = self.motorId, jointName = self.parent+"_"+self.child)


    @staticmethod
    def generateJointDimensions(parent, side):

        if side == CUBESIDE.positiveLength:
            return [parent.length/2, 0, 0], "0 0 1"
        elif side == CUBESIDE.negativeLength:
            return [-parent.length/2, 0, 0], "0 0 1"
        elif side == CUBESIDE.positiveWidth:
            return [0, parent.width/2, 0], "0 0 1" 
        elif side == CUBESIDE.negativeWidth:
            return [0, -parent.width/2, 0], "0 0 1"   
        elif side == CUBESIDE.positiveHeight:
            return [0, 0, parent.height/2], "0 1 0"   
        elif side == CUBESIDE.negativeHeight:
            return [0, 0, -parent.height/2], "0 1 0"
        else:
            raise TypeError("Invalid type")