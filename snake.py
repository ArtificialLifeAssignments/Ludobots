import numpy as np
import pyrosim.pyrosim as pyrosim
import os, time
import constants as c

class SNAKE:
    def __init__(self, id):
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        self.myId = id


    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myId) +  " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myId) + ".txt"

        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        f = open(fitnessFileName, "r")
        self.fitness = float(f.read())
        f.close()
        os.system("rm " + fitnessFileName)
        os.system("rm body" + str(self.myId) + ".urdf")
        os.system("rm world" + str(self.myId) + ".sdf")

    def Create_World(self):
        x, y, z = -2, 2, 0.1
        length, width, height = 1, 1, 1
        pyrosim.Start_SDF("world" + str(self.myId) + ".sdf")
        pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body" + str(self.myId) + ".urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_Backleg", parent= "Torso",child = "Backleg",
                type = "revolute", position = [0, -0.5, 1], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name="Backleg", pos=[0, -0.5, 0], size=[0.2, 1.0, 0.2])
        pyrosim.Send_Joint(name="Torso_Frontleg", parent= "Torso",child = "Frontleg",
                type = "revolute", position = [0, 0.5, 1], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name="Frontleg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])

        #First section legs
        pyrosim.Send_Joint(name="Frontleg_Frontlowerleg", parent= "Frontleg",child = "Frontlowerleg",
                type = "revolute", position = [0, 1, 0], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name="Frontlowerleg", pos=[0, 0.1, -0.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="Backleg_Backlowerleg", parent= "Backleg",child = "Backlowerleg",
                type = "revolute", position = [0, -1, 0], jointAxis= "1 0 0")
        pyrosim.Send_Cube(name="Backlowerleg", pos=[0, -0.1, -0.5], size=[0.2, 0.2, 1])

        for i in range(c.snakeSize):
            #Connector
            mult = str(i) if i != 0 else ""
            k = i+1
            adt = str(k)

            Mid = "Mid"+mult
            Torso = "Torso"+mult
            Torso_Mid = Torso + "_" + Mid

            position1 = [0.5, 0, 1] if i == 0 else [1, 0, 0]

            pyrosim.Send_Joint(name=Torso_Mid, parent= Torso, child = Mid,
                    type = "revolute", position = position1, jointAxis= "0 0 1")
            pyrosim.Send_Cube(name=Mid, pos=[0.2, 0, 0], size=[0.4, 0.7, 0.4])
            pyrosim.Send_Joint(name=Mid+"_"+"Torso"+adt, parent= Mid, child = "Torso"+adt,
                    type = "revolute", position = [0.4, 0, 0], jointAxis= "0 0 1")
            
            #SecondBody
            pyrosim.Send_Cube(name="Torso"+adt, pos=[0.5, 0, 0], size=[1, 1, 1])
            pyrosim.Send_Joint(name="Torso"+ adt + "_Backleg" + adt, parent= "Torso"+adt,child = "Backleg"+adt,
                    type = "revolute", position = [0.5, -0.5, 0], jointAxis= "1 0 0")
            pyrosim.Send_Cube(name="Backleg"+adt, pos=[0, -0.5, 0], size=[0.2, 1.0, 0.2])
            pyrosim.Send_Joint(name="Torso"+ adt + "_Frontleg" + adt, parent= "Torso"+adt,child = "Frontleg"+adt,
                    type = "revolute", position = [0.5, 0.5, 0], jointAxis= "1 0 0")
            pyrosim.Send_Cube(name="Frontleg"+adt, pos=[0, 0.5, 0], size=[0.2, 1, 0.2])

            #Second section legs
            pyrosim.Send_Joint(name="Frontleg" + adt + "_Frontlowerleg" + adt, parent= "Frontleg"+ adt,child = "Frontlowerleg"+adt,
                    type = "revolute", position = [0, 1, 0], jointAxis= "1 0 0")
            pyrosim.Send_Cube(name="Frontlowerleg"+adt, pos=[0, 0.1, -0.5], size=[0.2, 0.2, 1])
            pyrosim.Send_Joint(name="Backleg" + adt + "_Backlowerleg"+ adt, parent= "Backleg"+ adt,child = "Backlowerleg"+ adt,
                    type = "revolute", position = [0, -1, 0], jointAxis= "1 0 0")
            pyrosim.Send_Cube(name="Backlowerleg"+ adt, pos=[0, -0.1, -0.5], size=[0.2, 0.2, 1])




        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myId) + ".nndf")

        id = 0

        linkTemplateNames = ["Torso", "Backleg", "Frontleg", "Frontlowerleg", "Backlowerleg"]

        jointTemplateNames = [["Torso", "Backleg"], ["Torso", "Frontleg"], ["Frontleg", "Frontlowerleg"], ["Backleg", "Backlowerleg"]]

        linkNames = []
        jointNames = []

        for i in range(c.snakeSize+1):
            for link in linkTemplateNames:
                if i==0:
                    linkNames.append(link)
                else:
                    linkNames.append(link+str(i))

            if i < c.snakeSize:
                mult = "Mid" + str(i) if i != 0 else "Mid"
                linkNames.append(mult)

        for i in range(c.snakeSize+1):
            for left, right in jointTemplateNames:
                if i == 0:
                    jointNames.append(left+"_"+right)
                else:
                    jointNames.append(left+str(i)+"_"+right+str(i))
            
            if i < c.snakeSize and i > 0:
                mult = "Mid" + str(i) if i != 0 else "Mid"
                if i == 1:
                    jointNames.append("Torso_Mid")
                    jointNames.append("Mid_Torso1")
                else:
                    j = i - 1
                    jointNames.append("Torso" + str(j) +"_Mid" + str(j))
                    jointNames.append("Mid"+ str(j) + "_Torso"+str(i))



        for link in linkNames:
            pyrosim.Send_Sensor_Neuron(name = id , linkName = link)
            id += 1
        
        for joint in jointNames:
            pyrosim.Send_Motor_Neuron( name = id , jointName = joint)
            id+=1

        c.numSensorNeurons = len(linkNames)
        c.numMotorNeurons = len(jointNames)

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn+c.numSensorNeurons,
                        weight = self.weights[currentRow][currentColumn])
    
        pyrosim.End()

    def Mutate(self):
        indexRow = np.random.randint(0, c.numSensorNeurons-1)
        indexColumn = np.random.randint(0, c.numMotorNeurons-1)

        self.weights[indexRow][indexColumn] = np.random.random() * 2 -1

    def Set_ID(self, id):
        self.myId = id




