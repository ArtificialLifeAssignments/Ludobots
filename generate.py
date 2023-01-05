import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("box.sdf")

length, width, height = 1, 1, 1

pyrosim.Send_Cube(name="Box", pos=[0, 0, 0.5], size=[length, width, height])

pyrosim.End()
