import pickle
import sys
import time
import constants as c

class playSavedPickles:
        def __init__(self, seed = 1):
            self.seed = seed

    
        def loadPickleData(self, fileName):
            with open(fileName, 'rb') as f:
                thePickle =  pickle.load(f)
            f.close()
            return thePickle
    
        def playInitialPickleData(self):
            for i in range(c.populationSize):
                thePickle = self.loadPickleData("{}seed_{}_initial_parent_{}.p".format(c.initialParentsFilePath, self.seed, i))
                thePickle.Start_Simulation("GUI")
                time.sleep(20)
                thePickle.Wait_For_Simulation_To_End()

        def playFinalPickleData(self):
            for i in range(c.populationSize):
                thePickle = self.loadPickleData("{}seed_{}_final_state_{}.p".format(c.finalParentsFilePath, self.seed, i))
                thePickle.Start_Simulation("GUI")
                time.sleep(20)
                thePickle.Wait_For_Simulation_To_End()

        def playBestPickleData(self):
            thePickle = self.loadPickleData("{}seed_{}_best_state.p".format(c.bestStateFilePath, self.seed))
            thePickle.Start_Simulation("GUI")
            time.sleep(20)
            thePickle.Wait_For_Simulation_To_End()
                

# seed = sys.argv[1]
for i in range(1, 10):
    playSavedPickle = playSavedPickles(i)
    playSavedPickle.playBestPickleData()
# playSavedPickles = playSavedPickles(int(seed))
# playSavedPickles.playInitialPickleData()
# # playSavedPickles.playFinalPickleData()
# playSavedPickles.playBestPickleData()
