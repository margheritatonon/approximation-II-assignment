import numpy as np
import matplotlib.pyplot as plt
import scipy.fft

#defining all parameters:
frequency = 5
sampling_frequency = 1

#time vector from 0 to 2
def generate_signal(t_end, frequency, plot = False):
    """
    Generates a sine wave from t = 0 to t=t_end with frequency defined by the frequency parameter.
    If plot = True, plots the generated sine wave.
    Returns the time array t and the x(t) sinusoid.
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
    return t, x

t_continuous, x_continuous = generate_signal(2, frequency, plot = True)
print(f"len(x_continuous) = {len(x_continuous)}")

#we know that to avoid aliasing, we should have fs > 2 * B
nyquist_shannon_threshold = 2 * frequency 
print(f"fs >= nyquist_shannon_threshold: {sampling_frequency >= nyquist_shannon_threshold}")

def sample_signal(x, t, fs, plot = False):
    """
    Samples the continuous time signal x at a rate fs.
    t: the time interval of the sampled signal x
    Returns the time and amplitude arrays of the sampled signal
    """
    Ts = 1/fs #defining the sampling period
    t_sampled = np.arange(t[0], t[-1], Ts) #the sampled time points
    x_sampled = np.interp(t_sampled, t, x) #using 
    if plot == True:
        plt.plot(t, x, label = "Continuous")
        plt.scatter(t_sampled, x_sampled, label = "Sampled", color = "red")
        plt.title(f"Sampled Continuous Time Signal with Sampling Frequency {fs} Hz")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        #plt.legend()
        plt.show()
    return t_sampled, x_sampled

sample_signal(x_continuous, t_continuous, sampling_frequency, plot = True)