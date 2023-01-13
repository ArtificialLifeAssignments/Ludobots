import numpy
import matplotlib.pyplot as plt

backLegSensorValues = numpy.load("data/sensor.npy")
frontLegSensorValues = numpy.load("data/frontsensor.npy")

plt.plot(backLegSensorValues, label="backLegSensor", linewidth=2)
plt.plot(frontLegSensorValues, label="frontLegSensor")

plt.legend()
plt.show()