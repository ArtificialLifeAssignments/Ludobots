import numpy
import matplotlib.pyplot as plt

backLegSensorValues = numpy.load("data/sensor.npy")
frontLegSensorValues = numpy.load("data/frontsensor.npy")

frontLegTargetAngles = numpy.load("data/frontlegtargetangles.npy")
backLegTargetAngles = numpy.load("data/backlegtargetangles.npy")

# plt.plot(backLegSensorValues, label="backLegSensor", linewidth=2)
# plt.plot(frontLegSensorValues, label="frontLegSensor")
plt.plot(frontLegTargetAngles, label="frontLegTargetAngles")
plt.plot(backLegTargetAngles, label="backLegTargetAngles")

plt.legend()
plt.show()