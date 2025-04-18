import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift

#defining all parameters:
frequency = 5
sampling_frequency = 11
t_end = 2

#1: CREATING THE CONTINUOUS TIME SIGNAL
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
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()
    return t, x

t_continuous, x_continuous = generate_signal(t_end, frequency, plot = True)
print(f"len(x_continuous) = {len(x_continuous)}")

#2: SAMPLING
#we know that to avoid aliasing, we should have fs > 2 * B
nyquist_shannon_threshold = 2 * frequency 
print(f"fs >= nyquist_shannon_threshold: {sampling_frequency >= nyquist_shannon_threshold}")

def sample_signal(x, t, fs, plot_one = False, plot_two = False):
    """
    Samples the continuous time signal x at a sampling frequency fs.
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
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.grid(True)
        #plt.legend()
        plt.show()
    if plot_two == True:
        plt.stem(t_sampled, x_sampled, linefmt='r', markerfmt='ro', basefmt='None')
        plt.title(f"Sampled Signal with Sampling Frequency {fs} Hz")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.show()
    return t_sampled, x_sampled

t_sampled, x_sampled = sample_signal(x_continuous, t_continuous, sampling_frequency, plot_one = True, plot_two = True)

#3: FOURIER TRANSFORM
#Applying the Fourier Transform to visualize the continuous and the sampled signal
#we need to compute the FFT of the signals

#TODO: not sure if this function is going to be useful
def continuous_fourier_transform():
    pass

#TODO: here there are some bugs with the plot (e.g. at parameter values freq = 5, sampling freq = 11)

def sampled_fourier_transform(x_sampled, sampling_freq, num_duplicates, plot = False):
    """
    Returns the Fast Fourier Transform array (xf) and the corresponding __ values.
    If plot == True, plots the frequency domain plot, and num_duplicates duplicates of the frequency.
    """
    n = len(x_sampled)
    print(n)
    yf = fft(x_sampled)
    print(yf)
    xf = fftfreq(n, 1 / sampling_freq)
    if plot == True:
        magnitude = np.abs(yf)
        xf_shifted = fftshift(xf)
        magnitude_shifted = fftshift(magnitude)

        total_span = sampling_freq
        xf_tiled = []
        magnitude_tiled = []

        for i in range(-num_duplicates, num_duplicates + 1):
            xf_tiled.extend(xf_shifted + i * total_span)
            magnitude_tiled.extend(magnitude_shifted)
        
        plt.figure(figsize=(10, 4))
        plt.plot(xf_tiled, magnitude_tiled)
        plt.title("Frequency Domain Representation of Sampled Signal")
        plt.xlabel("Frequency (Hertz)")
        plt.grid(True)
        plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
        plt.show()

        #plt.plot(xf, np.abs(yf)) #we need to do np.abs on yf because its values are complex
        #plt.title("Frequency Domain Representation of Sampled Signal")
        #plt.xlabel("Frequency (Hertz)")
        #plt.show()
    return yf, xf

#the representation of our signal in the frequency domain is
#1/Ts * the sum from n = -inf to inf of  X(f - n/Ts) 
#and this is why the representation of the sampled signal in the frequency domain is the fourier transform of the original function but duplicated and shifted over

yf, xf = sampled_fourier_transform(x_sampled, sampling_frequency, num_duplicates = 2, plot = True)


#RECONSTRUCTION
#TODO: create a function that plots only the filtered frequencies, but not the other "aliased" ones --> and if we do have aliasing show what the output of the ideal filter is
#I think here I meant in the frequency domain

#We now reconstruct the original signal from the sampled signal.
#the signal can be recovered applying an (ideal band pass) filter --> in time domain this looks like the sinc function
def reconstruction(x_sampled, t_sampled, x_continuous, t_s, plot = False):
    """
    Returns the reconstructed signal from the sampled signal x_sampled, using t_sampled (the discrete timesteps of the sampled signal) and t_s (the time axis that we want the signal to be reconstructed on).
    If plot = True, plots the reconstructed signal along with the original signal and sampled points.
    """

    Fs = 1/t_sampled[1]
    x_s = np.zeros(len(t_s))
    for n in range(0, len(t_sampled)):
        x_s = x_s + x_sampled[n] * np.sinc(Fs * t_s - n) #this is the filter - but we are adding the frequencies together
    
    if plot == True:
        plt.plot(t_s, x_s, label = "Reconstructed")
        plt.plot(t_s, x_continuous, label = "Original", color = "Red", ls="--", alpha = 0.7)
        plt.title(f"Reconstructed Signal (sampling frequency {sampling_frequency} Hz) versus Original Signal (frequency {frequency} Hz)")
        plt.xlabel("Time")
        plt.legend() #TODO: add a legend location (or specify in the title)
        plt.show() #TODO: understand why when we have freq = 5 and then sampling freq = 12 (shannon nyquist MET), we do not get the exact same signal. --> is it because of quantization errors?

    return x_s

x_s = reconstruction(x_sampled, t_sampled, x_continuous, t_continuous, plot = True)