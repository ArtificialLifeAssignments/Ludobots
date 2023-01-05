import pybullet as p
import time

physicsClient = p.connect(p.GUI)

p.loadSDF("box.sdf")

for _ in range(10000):
    p.stepSimulation()
    time.sleep(1/60)

p.diconnect()

