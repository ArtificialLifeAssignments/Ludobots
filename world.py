import pybullet as p
class WORLD:
    def __init__(self, solutionId):
        
        self.planeId = p.loadURDF("plane.urdf")
        p.loadSDF("world" + str(solutionId) + ".sdf")