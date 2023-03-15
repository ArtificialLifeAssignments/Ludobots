from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c


for i in range(2, 10):
    phc = PARALLEL_HILL_CLIMBER(i+1) # Seed starts from 1 to numberOfSeedFiles
    phc.Evolve()