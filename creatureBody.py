import pyrosim.pyrosim as pyrosim
import constants as c
import random
from cubeSide import CUBESIDE

class CREATUREBODY:
    def __init__(self, id, connectorFace, sensors, creationStatistics):
        self.id = id
        self.connectorFace = connectorFace
        self.sensors = sensors
        self.creationStatistics = creationStatistics

    def genBody(self):

        thePos, theSize = self.getPositionAndSize()

        if self.id in self.sensors:
            pyrosim.Send_Cube(name=str(self.id), pos=thePos, size=theSize)
            self.creationStatistics.sensors.append(self.id)
        else:
            pyrosim.Send_Cube(name=str(self.id),  pos=thePos, size=theSize, c1='<material name="Cyan">',c2='    <color rgba="0 1.0 1.0 1.0"/>')
            


    def getPositionAndSize(self):

        length = random.uniform(c.lowerBound, c.upperBound)
        width = random.uniform(c.lowerBound, c.upperBound) 
        height = random.uniform(c.lowerBound, c.upperBound)

        self.length = length
        self.width = width
        self.height = height
        
        if self.connectorFace == CUBESIDE.positiveLength:
            return [length/2, 0, 0], [length, width, height]
        elif self.connectorFace == CUBESIDE.negativeLength:
            return [-length/2, 0, 0], [length, width, height]
        elif self.connectorFace == CUBESIDE.positiveWidth:
            return [0, width/2, 0], [length, width, height]
        elif self.connectorFace == CUBESIDE.negativeWidth:
            return [0, -width/2, 0], [length, width, height]
        elif self.connectorFace == CUBESIDE.positiveHeight:
            return [0, 0, height/2], [length, width, height]
        elif self.connectorFace == CUBESIDE.negativeHeight:
            return [0, 0, -height/2], [length, width, height]
        else:
            raise TypeError("Invalid type")
        
    def generateBrain(self):
        if self.id in self.sensors:
            pyrosim.Send_Sensor_Neuron(name = self.id , linkName =str(self.id))
 


   

    
