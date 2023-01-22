import pybullet_data
import pybullet as p
import time
import constants as c

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self):

        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT()

        

    def RUN(self):
        for i in range(c.numberOfIterations):
            p.stepSimulation()
            self.robot.sense(i)
            self.robot.Act(i)
            time.sleep(1/60)
        
    def __delete__(self):
        p.diconnect()

    
