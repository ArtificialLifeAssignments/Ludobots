from hillclimber import HILL_CLIMBER
import os


hc = HILL_CLIMBER()
hc.Evolve()

# for i in range(2):
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")