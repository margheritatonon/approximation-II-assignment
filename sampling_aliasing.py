import numpy as np
import matplotlib.pyplot as plt
import scipy.fft

#time vector from 0 to 2
def generate_signal(t_end, frequency, plot = False):
    """
    Generates a sine wave from t = 0 to t=t_end with frequency defined by the frequency parameter.
    If plot = True, plots the generated sine wave.
    Returns the x(t) sinusoid.
    """
    t = np.linspace(0, t_end, 10000)
    x = np.sin(2 * np.pi * frequency * t)
    if plot == True:
        plt.plot(t, x)
        plt.title(f"Continuous Time Signal - Sine Wave With Frequency {frequency} Hertz")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()
    return x

frequency = 5
x_continuous = generate_signal(2, frequency, plot = True)

#we know that to avoid aliasing, we should have fs > 2 * B
nyquist_shannon_threshold = 2 * frequency 

#sampling:
sampling_frequency = 1
print(f"fs >= nyquist_shannon_threshold: {sampling_frequency >= nyquist_shannon_threshold}")

def sample_signal():
    """
    Samples the continuous time signal x at a rate fs
    Returns the array of the sampled signal
    """
    pass