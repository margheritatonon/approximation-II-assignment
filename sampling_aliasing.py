import numpy as np
import matplotlib.pyplot as plt

#time vector from 0 to 2
t = np.linspace(0, 2, 10000)

frequency = 5 
x = np.sin(2 * np.pi * frequency * t) #this defines the sine wave from t = 0 to t = 2

plt.plot(t, x)
plt.title(f"Continuous Time Signal - Sine Wave With Frequency {frequency} Hertz")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

#we know that to avoid aliasing, we should have fs > 2 * B
nyquist_shannon_threshold = 2 * frequency 
