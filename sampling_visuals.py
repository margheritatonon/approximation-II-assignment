import numpy as np
import matplotlib.pyplot as plt
from sampling_aliasing import generate_signal

frequency = 2
sampling_frequency = 5
t_continuous, x_continuous = generate_signal(2, frequency, plot = True)

def sample_signal(x, t, fs, plot_one = False):
    """
    Samples the continuous time signal x at a rate fs.
    t: the time interval of the sampled signal x
    Returns the time and amplitude arrays of the sampled signal
    If plot == True, plots the continuous signal along with the sampled points.
    """
    Ts = 1/fs #defining the sampling period
    t_sampled = np.arange(t[0], t[-1], Ts) #the sampled time points
    x_sampled = np.interp(t_sampled, t, x) #using np.interp to sample

    if plot_one == True:
        plt.plot(t, x, label = "Original")
        #plt.scatter(t_sampled, x_sampled, label = "Sampled", color = "red")
        plt.stem(t_sampled, x_sampled, linefmt='r', markerfmt='ro', basefmt='None', label = "Sampled")
        plt.title(f"Original Signal versus Sampled Signal (Sampling Frequency {fs} Hertz)", size = 25)
        plt.xlabel("Time (s)", size = 20)
        plt.ylabel("Amplitude", size = 20)
        plt.grid(True)
        plt.legend()
        plt.show()
    
    return t_sampled, x_sampled

sample_signal(x_continuous, t_continuous, sampling_frequency, plot_one = True)