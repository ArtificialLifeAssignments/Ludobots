import pyrosim.pyrosim as pyrosim

# pyrosim.Start_SDF("world.sdf")
# x, y, z = 0, 0, 0.1
# length, width, height = 1, 1, 1
# pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
# pyrosim.End()


def Create_World():
    x, y, z = -2, 2, 0.1
    length, width, height = 1, 1, 1
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
    pyrosim.End()

Create_World()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 0.1], size=[1, 1, 1])
    pyrosim.End()

Create_Robot()
