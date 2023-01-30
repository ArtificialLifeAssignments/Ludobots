from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionId = sys.argv[2]

simulation = SIMULATION(directOrGUI, solutionId)
simulation.RUN()
simulation.Get_Fitness()

