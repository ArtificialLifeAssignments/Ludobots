import pyrosim.pyrosim as pyrosim
import os, time
import constants as c
import random

class CREATURE:
    def __init__(self, id, seed=1676127262.929452):
        self.myId = id
        random.seed(seed)
        self.Generate_Random_Morphology();

    def Generate_Random_Morphology(self):
        self.numberOfSections = random.randint(c.minimumSections, c.maximumSections)
        self.numberOfSensors = random.randint(0, self.numberOfSections)

        self.sensorPositions = set(random.sample([i for i in range(self.numberOfSections)], self.numberOfSensors))

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
        pyrosim.Start_SDF("world" + str(self.myId) + ".sdf")
        pyrosim.End()

    def Generate_Body(self):
        length = random.uniform(c.lowerBound, c.upperBound)
        width = random.uniform(c.lowerBound, c.upperBound) 
        height = random.uniform(c.lowerBound, c.upperBound)
        index = 0
        pyrosim.Start_URDF("body" + str(self.myId) + ".urdf")


        if index in self.sensorPositions:
            pyrosim.Send_Cube(name="Torso"+str(index), pos=[0, 0, 0.5], size=[length, width, height])
        else:
            pyrosim.Send_Cube(name="Torso"+str(index), pos=[0, 0, 0.5], size=[length, width, height], c1='<material name="Cyan">',c2='    <color rgba="0 1.0 1.0 1.0"/>')

        index2 = index + 1
        pyrosim.Send_Joint(name="Torso"+str(index)+"_Torso"+str(index2), parent="Torso"+str(index), child ="Torso"+str(index2),
                     type = "revolute", position = [length/2, 0, 0.5], jointAxis= "0 0 1")

        for index in range(1, self.numberOfSections):
            
            length = random.uniform(c.lowerBound, c.upperBound)
            width = random.uniform(c.lowerBound, c.upperBound) 
            height = random.uniform(c.lowerBound, c.upperBound)
            if index in self.sensorPositions:
                pyrosim.Send_Cube(name="Torso"+str(index), pos=[length/2, 0, 0], size=[length, width, height])
            else:
                pyrosim.Send_Cube(name="Torso"+str(index), pos=[length/2, 0, 0], size=[length, width, height], c1='<material name="Cyan">',c2='    <color rgba="0 1.0 1.0 1.0"/>')
            index2 = index + 1

            if index != self.numberOfSections-1:
                pyrosim.Send_Joint(name="Torso"+str(index)+"_Torso"+str(index2), parent="Torso"+str(index), child ="Torso"+str(index2),
                    type = "revolute", position = [length, 0, 0], jointAxis= "0 0 1")

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myId) + ".nndf")

        id = 0
        linkNames = []
        jointNames = []

        for i in range(self.numberOfSections):
            linkNames.append("Torso"+str(i))

        for i in range(self.numberOfSections-1):
            l1 = "Torso"+str(i)
            k = i+1
            l2 = "_Torso"+str(k)
            jointNames.append(l1+l2)

        for index, link in enumerate(linkNames):
            if index in self.sensorPositions:
                pyrosim.Send_Sensor_Neuron(name = index , linkName = link)
        
        id = self.numberOfSections
        motorId = []
        for joint in jointNames:
            pyrosim.Send_Motor_Neuron(name = id , jointName = joint)
            motorId.append(id)
            id+=1
        
        c.numSensorNeurons = self.numberOfSensors
        c.numMotorNeurons = self.numberOfSections-1

        for sensor in self.sensorPositions:
            for motor in motorId:
                pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight = random.random() * 2 -1)
    
        pyrosim.End()

    def Mutate(self):
        pass
        # indexRow = np.random.randint(0, c.numSensorNeurons-1)
        # indexColumn = np.random.randint(0, c.numMotorNeurons-1)

        # self.weights[indexRow][indexColumn] = np.random.random() * 2 -1

    def Set_ID(self, id):
        self.myId = id







