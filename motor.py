import numpy
import constants as c
import pybullet as p
import pyrosim.pyrosim as pyrosim

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.maxForce = c.frontLegMaxForce

    def Set_Value(self, desiredAngle, robot):
        pyrosim.Set_Motor_For_Joint(bodyIndex=robot.robotId, jointName=self.jointName, 
                        controlMode=p.POSITION_CONTROL, targetPosition=desiredAngle, maxForce=self.maxForce)
       