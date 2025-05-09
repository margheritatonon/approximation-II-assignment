import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sampling_aliasing import generate_signal, sampled_fourier_transform


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

def left_right_signal(x, t, fs, plot = False):
    """
    Sampled the continuous time signal x at a rate fs.
    t: the time interval of the sampled signal x
    If plot == True, plots the original signal on the left and the sampled signal on the right.
    """
    Ts = 1/fs 
    t_sampled = np.arange(t[0], t[-1], Ts)
    x_sampled = np.interp(t_sampled, t, x)

    if plot == True:
        fig, axs = plt.subplots(1, 2, figsize=(14, 5))

        axs[0].plot(t, x, label="Original", color='blue')
        axs[0].set_title(f"Original Signal ({frequency} Hz)", fontsize=25)
        axs[0].set_xlabel("Time (s)", fontsize=18)
        axs[0].set_ylabel("Amplitude", fontsize=18)
        axs[0].axhline(0, ls = "--", color="gray")
        axs[0].grid(True)
        #axs[0].legend()

        axs[1].stem(t_sampled, x_sampled, linefmt='r', markerfmt='ro', basefmt='None', label="Sampled")
        axs[1].set_title(f"Sampled Signal ({sampling_frequency} Hz)", fontsize=25)
        axs[1].set_xlabel("Time (s)", fontsize=18)
        #axs[1].set_ylabel("Amplitude", fontsize=14)
        axs[1].axhline(0, ls = "--", color="gray")
        axs[1].grid(True)
        #axs[1].legend()

        plt.tight_layout()
        plt.show()
    
    return t_sampled, x_sampled


#TODO: make it compatible with the function that plots the different frequencies
#creating a filtering function just to visualize the filtered frequencies in the frequency domain
def filtering(yf:np.array, xf:np.array, fl:float, fh:float, plot = False):
    """
    Uses an ideal band-pass filter to select the frequencies between fl and fh of the fourier transform of the signal yf, using the frequencies of the fourier transform of the signal xf.
    Returns the filtered array.
    If plot == True, then a plot of the filtered frequencies in the frequency domain is shown.
    """
    mask = (np.abs(xf) >= fl) & (np.abs(xf) <= fh)
    yf_filtered = yf.copy()
    yf_filtered = np.copy(yf)
    yf_filtered[~mask] = 0 #makes all of the frequencies outside of the filter = 0

    if plot == True:
        plt.figure(figsize=(10, 4))
        plt.plot(xf, np.abs(yf), label="Original")
        plt.plot(xf, np.abs(yf_filtered), label="Filtered", ls = "--")
        plt.title("Frequency Domain Filtering")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.grid(True)
        plt.legend()
        plt.show()

    return yf_filtered


def frequency_domain_plot(x_continuous, t_continuous):
    """
    Plots the frequency domain representation of the continuous signal.
    """
    dt = t_continuous[1] - t_continuous[0]
    fs = 1 / dt #the sampling frequency
    N = len(x_continuous) #number of samples
    X = np.fft.fft(x_continuous)
    X_magnitude = np.abs(X) / N
    freqs = np.fft.fftfreq(N, d=dt)

    plt.figure(figsize=(15, 5))
    plt.plot(freqs, X_magnitude, color = "black")
    plt.title(f"Frequency Domain Representation of Time Continuous Signal", fontsize=25)
    plt.xlabel("Frequency (Hz)", fontsize=18)
    plt.ylabel("Magnitude", fontsize=18)
    plt.grid(True)
    plt.xlim(-10, 10)
    plt.show()


if __name__ == "__main__":

    #defining parameters
    frequency = 2
    sampling_frequency = 10

    #script import functions
    t_continuous, x_continuous = generate_signal(2, frequency, signal_type="single", plot = False)
    t_sampled, x_sampled = sample_signal(x_continuous, t_continuous, sampling_frequency)
    yf, xf = sampled_fourier_transform(x_sampled, sampling_frequency, num_duplicates = 2)

    #functions of the current script
    filtering(yf, xf, 1, 5, plot = False)

    #frequency_domain_plot(x_continuous, t_continuous)

    left_right_signal(x_continuous, t_continuous, sampling_frequency, plot = True)
