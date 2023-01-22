import constants as c
import numpy
import pyrosim.pyrosim as pyrosim

class SENSOR:

    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.numberOfIterations)

    def Get_Value(self, index):
        self.values[index] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

        if index+1 == c.numberOfIterations:
            print(self.values)
    
    def Save_Values(self):
        numpy.save("data/"+str(self.linkName)+".npy", self.values)