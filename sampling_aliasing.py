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

def sample_signal(x, t, fs, plot_one = False, plot_two = False):
    """
    Samples the continuous time signal x at a rate fs.
    t: the time interval of the sampled signal x
    Returns the time and amplitude arrays of the sampled signal
    If plot_one == True, plots the continuous signal along with the sampled points.
    If plot_two == True, plots the sampled points only.
    """
    Ts = 1/fs #defining the sampling period
    t_sampled = np.arange(t[0], t[-1], Ts) #the sampled time points
    x_sampled = np.interp(t_sampled, t, x) #using np.interp to sample

    if plot_one == True:
        plt.plot(t, x, label = "Continuous")
        #plt.scatter(t_sampled, x_sampled, label = "Sampled", color = "red")
        plt.stem(t_sampled, x_sampled, linefmt='r', markerfmt='ro', basefmt='None')
        plt.title(f"Sampled Continuous Time Signal with Sampling Frequency {fs} Hz")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        #plt.legend()
        plt.show()
    if plot_two == True:
        plt.stem(t_sampled, x_sampled, linefmt='r', markerfmt='ro', basefmt='None')
        plt.title(f"Sampled Signal with Sampling Frequency {fs} Hz")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()
    return t_sampled, x_sampled

sample_signal(x_continuous, t_continuous, sampling_frequency, plot_one = True, plot_two = True)


#Applying the Fourier Transform to visualize the continuous and the sampled signal
def continuous_fourier_transform():
    pass

def sampled_fourier_transform():
    pass
#the representation of our signal in the frequency domain is
#1/Ts * the sum from n = -inf to inf of  X(f - n/Ts) 
#and this is why the representation of the sampled signal in the frequency domain is the fourier transform of the original function but duplicated and shifted over
