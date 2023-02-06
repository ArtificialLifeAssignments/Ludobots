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

numberOfGenerations = 10

populationSize = 10

snakeSize = 2

def getJoints(snakeSize):

    if snakeSize+1 == 1:
        return 4
    else:
        return (snakeSize * 6) + 4
numMotorNeurons = getJoints(snakeSize)
numSensorNeurons = numMotorNeurons + 1


motorJointChange = 0.2

