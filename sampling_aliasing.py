import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift

#defining all parameters:
frequency = 5
sampling_frequency = 12
t_end = 2

#1: CREATING THE CONTINUOUS TIME SIGNAL
#time vector from 0 to 2
def generate_signal(t_end, frequency, plot = False):
    """
    Generates a sine wave from t = 0 to t = t_end with frequency defined by the frequency parameter.
    If plot = True, plots the generated sine wave.
    Returns the time array t and the x(t) sinusoid.
    """
    t = np.linspace(0, t_end, int(5000 * t_end))
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
print(f"fs >= nyquist_shannon_threshold: {sampling_frequency >= nyquist_shannon_threshold}") #just for checking

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

def sampled_fourier_transform(x_sampled, sampling_freq, num_duplicates, plot = False):
    """
    Returns the Fast Fourier Transform array (yf) and the corresponding frequncy values (xf).
    If plot == True, plots the frequency domain plot, and num_duplicates duplicates of the frequency.
    """
    n = len(x_sampled)
    yf = fft(x_sampled) #the fast fourier transform of the sampled signal
    xf = fftfreq(n, 1 / sampling_freq) #the corresponding frequencies of the sampled signal

    if plot == True:
        magnitude = np.abs(yf) #the modulus of the fourier transform of the sampled signal
        #for better visualization:
        xf_shifted = fftshift(xf) #rearranges the frequncies so that 0 is in the center
        magnitude_shifted = fftshift(magnitude) #rearranged magnitudes so 0 is in th center to match xf_shifted

        total_span = sampling_freq #the range between each repeated frequency spectrum

        #initializing:
        xf_tiled = []
        magnitude_tiled = []

        for i in range(-num_duplicates, num_duplicates + 1): #loops through to create copies for visualization
            xf_tiled.extend(xf_shifted + i * total_span) #adds each element of the iterable to the list individually
            magnitude_tiled.extend(magnitude_shifted)
        
        #plotting
        plt.figure(figsize=(10, 4))
        plt.plot(xf_tiled, magnitude_tiled)
        plt.title("Frequency Domain Representation of Sampled Signal")
        plt.xlabel("Frequency (Hertz)")
        plt.grid(True)
        plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
        plt.show()

    return yf, xf

yf, xf = sampled_fourier_transform(x_sampled, sampling_frequency, num_duplicates = 4, plot = True)


#4: RECONSTRUCTION
#We now reconstruct the original signal from the sampled signal.
#the signal can be recovered applying an (ideal band pass) filter --> in time domain this looks like the sinc function
def reconstruction(x_sampled, t_sampled, plot = False, x_continuous = None, t_s = None):
    """
    Returns the reconstructed signal from the sampled signal x_sampled, using t_sampled (the discrete timesteps of the sampled signal) and t_s (the time axis that we want the signal to be reconstructed on).
    If plot = True, plots the reconstructed signal along with the original signal and sampled points.
    """

    Fs = 1/(t_sampled[1] - t_sampled[0]) #calculates the sampling frequency

    x_s = np.zeros(len(t_s)) #initializing the reconstructed signal array
    for n in range(0, len(t_sampled)):
        x_s = x_s + x_sampled[n] * np.sinc(Fs * t_s - n) #this is the filter - but we are adding the frequencies together
    
    if plot == True:
        plt.plot(t_s, x_s, label = "Reconstructed")
        plt.plot(t_s, x_continuous, label = "Original", color = "Red", ls="--", alpha = 0.7)
        plt.title(f"Reconstructed Signal (sampling frequency {sampling_frequency} Hz) versus Original Signal (frequency {frequency} Hz)")
        plt.xlabel("Time")
        plt.legend(loc="upper left")
        plt.show()

    return x_s

x_s = reconstruction(x_sampled, t_sampled, plot = True, x_continuous=x_continuous, t_s=t_continuous)