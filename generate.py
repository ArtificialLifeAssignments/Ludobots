import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")



x, y, z = 0, 0, 0.1

for _ in range(8):
    x = 0
    for _ in range(8):
        length, width, height = 1, 1, 1
        z = 0.0
        for _ in range(8):
            pyrosim.Send_Cube(name="Box"+str(z), pos=[x, y, z], size=[length, width, height])
            z+=height
            length*=0.9
            width*=0.9
            height*=0.9
        x+=1
    y+=1
    
    

pyrosim.End()
