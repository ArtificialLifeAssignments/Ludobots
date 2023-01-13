from cmath import phase
from turtle import back
import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import random


backLegAmplitude = numpy.pi/4
backLegFrequency = 10
backLegPhaseOffset = 0


frontLegAmplitude = numpy.pi/4
frontLegFrequency = 10
frontLegPhaseOffset = numpy.pi/2

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

pyrosim.Prepare_To_Simulate(robotId)

backLegTargetAngles = numpy.sin(backLegFrequency * numpy.linspace(0, 2*numpy.pi, 1000) + backLegPhaseOffset) * backLegAmplitude
frontLegTargetAngles = numpy.sin(frontLegFrequency * numpy.linspace(0, 2*numpy.pi, 1000) + frontLegPhaseOffset) * frontLegAmplitude
numpy.save("data/frontlegtargetangles.npy",frontLegTargetAngles)
numpy.save("data/backlegtargetangles.npy",backLegTargetAngles)

for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Backleg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Frontleg")
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName="Torso_Backleg", controlMode=p.POSITION_CONTROL, 
                targetPosition=backLegTargetAngles[i], maxForce=50)
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName="Torso_Frontleg", 
                controlMode=p.POSITION_CONTROL, targetPosition=frontLegTargetAngles[i], maxForce=50)
    time.sleep(1/60)

numpy.save("data/sensor.npy", backLegSensorValues)
numpy.save("data/frontsensor.npy", frontLegSensorValues)


p.diconnect()

