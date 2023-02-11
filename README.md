# Randomly Generated Snake

This repository depicts a randomly generated snake with random number of body parts and random number of sensors placed randomly.
![](https://github.com/ArtificialLifeAssignments/Ludobots/blob/creature/crawler.gif)

## Generation diagram
![](https://github.com/ArtificialLifeAssignments/Ludobots/blob/snake/IMG_B374E8D96F93-1.jpeg)

## The major features:
 - The ant body is autogenerated and with a single change of variable it could be made to grow and chnage in size
 - The ant uses a paralel hill climbing evolution algorithm to build the best version of the quickest moving ant avoiding obstactles that could possibly
 slow it down
 - Ant has multiple mobile body parts thus maintains a variable amount of sensors
 
 ## Video link
  [Click on this link](https://youtu.be/lfw3tk1n8Ns)
  
 ## Fork and Set up Guide
 Fork and download the code from the createre branch. Any version of python `above 3.5` must be present in your system. After replication, using the terminal, navigate to the project folder and run the program using ```python3 search.py```. To modify the config file, navigate to the constants folder and 
 try modify the ```numberOfGenerations```  and or ```populationSize``` to test different levels of finetuning and the ```snakeSize``` Variable to change the size of the snake. 
 
 ## Future works
  -  Exploring different evolution algorithms to make the ant crawl faster
  - Adding a scaling variable controlling the size of the ant crawler to be able to fit more ant crawwlers in screen
  - Randomly generating an army of antcrawlers
  - Adding obstacles and training ant crawlers to navigate around them
 
 
 
