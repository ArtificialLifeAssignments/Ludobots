import numpy

numberOfIterations = 1000

backLegAmplitude = numpy.pi/4
backLegFrequency = 10
backLegPhaseOffset = 0


frontLegAmplitude = numpy.pi/4
frontLegFrequency = 10
frontLegPhaseOffset = numpy.pi/2

backLegMaxForce = 50
frontLegMaxForce = 50

numberOfGenerations = 1

populationSize = 1

snakeSize = 2

def getJoints(snakeSize):

    if snakeSize+1 == 1:
        return 4
    else:
        return (snakeSize * 6) + 4

numMotorNeurons = 0
numSensorNeurons = 0


motorJointChange = 0.5
maxGen = 0

numberOfChildGeneration = 3
numberOfDescendantsPerGeneration = 3

minimumSections = 20
maximumSections = 36

offsetForMotors = 100

upperBound = 0.5
lowerBound = 0.1

