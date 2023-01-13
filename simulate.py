from turtle import back
import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy





physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

pyrosim.Prepare_To_Simulate(robotId)

for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Backleg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("Frontleg")
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName="Torso_Backleg", controlMode=p.POSITION_CONTROL, targetPosition=0.0, maxForce=500)
    time.sleep(1/60)

numpy.save("data/sensor.npy", backLegSensorValues)
numpy.save("data/frontsensor.npy", frontLegSensorValues)

p.diconnect()

