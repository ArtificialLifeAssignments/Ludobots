import pyrosim.pyrosim as pyrosim
import constants as c
import random
from cubeSide import CUBESIDE

class CREATUREBODY:
    def __init__(self, id, parentId, currentGen, connectorFace, sensors, canHaveKids, creationStatistics, seed=0):
        self.id = id
        self.parentId = parentId
        self.currentGen = currentGen
        self.connectorFace = connectorFace
        self.sensors = sensors
        self.creationStatistics = creationStatistics
        self.children = []
        self.canHaveKids = canHaveKids
        self.genBody()

        if id in self.canHaveKids and currentGen < c.maxGen:
            self.generateChildren()
        print("created ", self.id)

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
        
        motorId = self.id + c.offsetForMotors
        pyrosim.Send_Motor_Neuron(name = motorId, jointName =str(self.parentId)+"_"+str(self.id))

        if self.id in self.sensors:
            pyrosim.Send_Sensor_Neuron(name = self.id , linkName =str(self.id))
        self.creationStatistics.motorId.append(motorId)

        for child in self.children: 
            child.generateBrain()
 


    def generateJoints(self):

        nameStr = str(self.id)+"_"+str(self.creationStatistics.nextId)

        for side in self.kidPosition:
            if side == self.connectorFace:
                continue
            elif side == CUBESIDE.positiveLength:
                pyrosim.Send_Joint(name=nameStr, parent=str(self.id), child=str(self.creationStatistics.nextId),
                     type = "revolute", position = [self.length/2, 0, 0], jointAxis= "0 0 1")
            elif side == CUBESIDE.negativeLength:
                pyrosim.Send_Joint(name=nameStr, parent=str(self.id), child=str(self.creationStatistics.nextId),
                     type = "revolute", position = [-self.length/2, 0, 0.5], jointAxis= "0 0 1")
            elif side == CUBESIDE.positiveWidth:
                pyrosim.Send_Joint(name=nameStr, parent=str(self.id), child=str(self.creationStatistics.nextId),
                     type = "revolute", position = [0, self.width/2, 0.5], jointAxis= "0 0 1") 
            elif side == CUBESIDE.negativeWidth:
                pyrosim.Send_Joint(name=nameStr, parent=str(self.id), child=str(self.creationStatistics.nextId),
                     type = "revolute", position = [0, -self.width/2, 0.5], jointAxis= "0 0 1")         
            elif side == CUBESIDE.positiveHeight:
                pyrosim.Send_Joint(name=nameStr, parent=str(self.id), child=str(self.creationStatistics.nextId),
                     type = "revolute", position = [0, 0, self.height/2], jointAxis= "0 1 0")      
            elif side == CUBESIDE.negativeHeight:
                pyrosim.Send_Joint(name=nameStr, parent=str(self.id), child=str(self.creationStatistics.nextId),
                     type = "revolute", position = [0, 0, -self.height/2], jointAxis= "0 1 0")
            else:
                raise TypeError("Invalid type")

    
    def generateChildren(self):

        self.kidPosition = set(random.sample([CUBESIDE(i+1) for i in range(6)], 1))
        self.generateJoints()
        for i in self.kidPosition:
            if i != self.connectorFace:
                self.creationStatistics.nextId += 1
                self.children.append(CREATUREBODY(self.creationStatistics.nextId-1, self.id, self.currentGen+1, 
                                                  i, self.sensors, self.canHaveKids, self.creationStatistics))


    
