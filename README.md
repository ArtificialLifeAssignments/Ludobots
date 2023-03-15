# Randomly Generated Snake

This repository depicts a randomly generated snake with random number of body parts and random number of sensors placed randomly. The links with the sensors are colored green and the rest are colored blue
![](https://github.com/ArtificialLifeAssignments/Ludobots/blob/snake/ass6Giphy.gif)

Linus Okoth
Human Intelligence is not the primary reason for the species' evolutionary success. It may have played a significant role; however, physical adaptations were a superior contributor to human survival.This fact, a foundational concept of human evolution, can be easily studied through the latest developments in Artificial Intellegince and its intersectection with bioengineering through the field called Artificial Life. 

Artificial life is a rapidly growing field that explores the creation of living systems in silico. A simpler definition is its the study of life not as it is, but as it could possibly be. Systems and algorithms designed in this field can be used to study biological systems and explore new avenues in other fields such as robotics, artificial intelligence, and bioengineering.

Finally to be able to define evolutionary success, I picked a mobility as a central theme in evaluating different species. 

Method

Algorithm and success Metrics
To be able to unbiasly measure the contribution of physical adaptations against intelligence towards evolutionary success(which I defined as mobility), I decided to pick Parallel Hill Climber, an optimization algorithm that closely resembles the evolutionary process. The parallel hill climber works by randomly generating a set of solutions, each of which us evaluated to determine its fitness score. The fitness score represents the quality of the solution, and the goal is to find the solution with the highest fitness score. My fitness score which is based on my evolutionary success(Mobility) is how far a spawned organism in my simulator is able to move away form the center.

Evolution Selection
Whilst applying the chosen algorithm, I decided to use indirect encoding to specify the evolutionary properties of each species in different generations. This means I followed  Karl Sims sample option to decide genotype encoding based on All vs best withion species fitness comparison. To explain this in code, At the start of the simulation, I generated 10 initial cubes,(parents) each to represent a different species, then regenerated the next ten each based on a lineage from the previous generation. I did this for 500 different generations in each stage modifying the parent morphology(the physical structure) or the brain(the weight from the sensors that trigger the motor neurons incharge of movement). I then comare the generated child to the best species of that generation to be able to pick the next best. 

At each stage of development where morphology was changed, I either, removed a cube that is in the edge together with the corresponding joint, or I added atmost 2 cubes at any random position on the body as described by the visual aid below:


On completion of that analysis, I redid the analysis another 10 times using a different random seed for each of the ten times. I then graphed the changes in the fitnesses of the best organism for each seed, producing ten graphs showing the results of each run. I also saved pickles of the 10 final best species state of each seed run in the data folder and further the pickle of the best species overall for each seed run.  I also pickled the initial 10 species parent of each random seed run. All of these pickled data can be viewed in the simulator by running the playSavedPickles module, that takes in a random seed from 1 - 10, and plays all the 10 initial parents in the simulator, then the final best 10 each corresponding to the fittest result of each species after 500 generation, then finally it plays the very best species of all the final 10. 

Results
The plotted results supported the hypothesis I wanted to observe. Since I paced every morphological change to coincide with even number generation, at close inspection of the graphs we see that all significant rises in fitness occurred at these points. Further we see the effects of the evolutionary algorithm, Parallel Hill climber. Since its an optimization algorithm that I configured with indirect encoding of genotypes by randomly searching the genotype space for the best fitness, we see that different parents achieve their best fitnesses at different points in evolution. Furthermore there is no single smooth curve of increasing fitness, but rather step increases because the search is not by continuous modification of morphology but by drastic changes.

![Graph1](https://github.com/ArtificialLifeAssignments/Ludobots/blob/final/data/fitnessGraphs/FitnessOfEvolvingRobotWithSeed1.png)



 ## Video link
  ![Click on this link](https://www.youtube.com/watch?v=l55aWs4c1nY&list=PLCGVHiz7oVMdL6_8B75XG6X2Wnk9bqsk1&index=18)
  
 ## Fork and Set up Guide
 - Fork and download the code from the createre branch. Any version of python `above 3.5` must be present in your system. After replication, using the terminal, navigate to the project folder and run the program using ```python3 search.py```. To modify the config file, navigate to the constants folder and 
 try modify the ```numberOfGenerations```  and or ```populationSize``` to test different levels of finetuning and the
 - To get the exact output, use the deafult seed value of random that I set as a default argument to the creature file otherwise you can modify the seed value to get other random productions
 
 
 ## Future works
  -  Exploring different evolution algorithms to make the snake crawl faster
  
  ## Acknowledgements
  - [Ludobots](https://www.reddit.com/r/ludobots/wiki/tipsandtricks/)

 
 
 
