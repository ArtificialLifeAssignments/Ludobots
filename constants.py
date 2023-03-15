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

minimumSections = 11
maximumSections = 13

offsetForMotors = 100

upperBound = 0.5
lowerBound = 0.1


numberOfGenerations = 500
populationSize = 10
numberOfSeedFiles = 10
fitnessFilePath = "data/fitnesses/"
fitnessGraphFilePath = "data/fitnessGraphs/"
initialParentsFilePath = "data/initialParents/"
bestStateFilePath = "data/bestState/"
finalParentsFilePath = "data/finalParents/"

