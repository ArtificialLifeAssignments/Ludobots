import pybullet_data
import pybullet as p
import time
import constants as c
from solution import SOLUTION

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self, directOrGUI, solutionId):

        if directOrGUI.lower() == "direct":
            self.directOrGUI = 1
        else:
            self.directOrGUI = 0

        if self.directOrGUI:
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT(solutionId)


    def RUN(self):
        for i in range(c.numberOfIterations):
            p.stepSimulation()
            self.robot.sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if not self.directOrGUI:
                time.sleep(1/60)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
        
        
    def __delete__(self):
        p.diconnect()

    
