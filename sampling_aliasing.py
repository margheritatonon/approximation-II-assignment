import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift

#defining all parameters:
frequency = 5
sampling_frequency = 7
t_end = 4
signal_type = "multiple" #choose between "single" or "multiple"

#1: CREATING THE CONTINUOUS TIME SIGNAL
#time vector from 0 to 2
def generate_signal(t_end, frequency, signal_type, plot = False):
    """
    Generates a sine wave from t = 0 to t = t_end with frequency defined by the frequency parameter.
    If plot = True, plots the generated sine wave.
    If signal_type = "single", generates a sine wave with frequency "frequency".
    If signal_type = "multiple", generates a sine wave with frequency "frequency" added to a sine wave with frequency "frequency/2".
    Returns the time array t and the x(t) sinusoid.
    """
    t = np.linspace(0, t_end, int(5000 * t_end))
    if signal_type == "single":
        x = np.sin(2 * np.pi * frequency * t)
        if plot == True:
            plt.figure(figsize=(12, 6))
            plt.plot(t, x)
            plt.title(f"Continuous Time Signal - Sine Wave With Frequency {frequency} Hertz", size = 25)
            plt.xlabel("Time", size = 20)
            plt.ylabel("Amplitude", size = 20)
            plt.grid(True)
            plt.show()
    elif signal_type == "multiple":
        x = np.sin(2 * np.pi * frequency * t) + np.sin(np.pi * frequency * t) #a sine wave with freq "frequency" added to a sine wave with freq "frequency/2"
        if plot == True:
            plt.figure(figsize=(15, 5))
            plt.plot(t, x)
            plt.title(f"Continuous Time Signal - Sum of Sine Waves With Frequencies {frequency/2} and {frequency} Hz", size = 25)
            plt.xlabel("Time", size = 20)
            plt.ylabel("Amplitude", size = 20)
            plt.grid(True)
            plt.show()
    else:
        raise ValueError("signal_type must be either 'single' or 'multiple'")
    return t, x

#2: SAMPLING
def sample_signal(x, t, fs, plot_one = False, plot_two = False, plot_three = False):
    """
    Samples the continuous time signal x at a sampling frequency fs.
    t: the time interval of the sampled signal x
    Returns the time and amplitude arrays of the sampled signal
    If plot_one == True, plots the continuous signal along with the sampled points.
    If plot_two == True, plots the sampled points only.
    If plot_three == True, plots plot 1 and plot 2 side by side.
    """
    Ts = 1/fs #defining the sampling period
    t_sampled = np.arange(t[0], t[-1], Ts) #the sampled time points
    x_sampled = np.interp(t_sampled, t, x) #using np.interp to sample

    if plot_one == True:
        plt.figure(figsize=(12, 6))
        plt.plot(t, x, label = "Continuous")
        #plt.scatter(t_sampled, x_sampled, label = "Sampled", color = "red")
        plt.stem(t_sampled, x_sampled, linefmt='r', markerfmt='ro', basefmt='None')
        plt.title(f"Sampled Continuous Time Signal with Sampling Frequency {fs} Hz", size = 25)
        plt.xlabel("Time", size = 20)
        plt.ylabel("Amplitude", size = 20)
        plt.grid(True)
        #plt.legend()
        plt.show()
    if plot_two == True:
        plt.figure(figsize=(12, 6))
        plt.stem(t_sampled, x_sampled, linefmt='r', markerfmt='ro', basefmt='None')
        plt.title(f"Sampled Signal with Sampling Frequency {fs} Hz", size = 25)
        plt.xlabel("Time", size = 20)
        plt.ylabel("Amplitude", size = 20)
        plt.grid(True)
        plt.show()
    if plot_three == True:
        fig, axs = plt.subplots(1, 2, figsize=(14, 5))

        axs[0].plot(t, x, label = "Continuous")
        axs[0].stem(t_sampled, x_sampled, linefmt='r', markerfmt='ro', basefmt='None')
        axs[0].set_xlabel("Time", size = 20)
        axs[0].set_ylabel("Amplitude", size = 20)
        axs[0].grid(True)

        axs[1].stem(t_sampled, x_sampled, linefmt='r', markerfmt='ro', basefmt='None')
        axs[1].set_xlabel("Time", size = 20)
        axs[1].grid(True)

        fig.suptitle(f"Sampled Signal with Sampling Frequency {fs} Hz", size = 30)
        plt.tight_layout()
        plt.show()

    return t_sampled, x_sampled

#3: FOURIER TRANSFORM
#Applying the Fourier Transform to visualize the continuous and the sampled signal
#we need to compute the FFT of the signals

def sampled_fourier_transform(x_sampled, sampling_freq, num_duplicates, plot = False):
    """
    Returns the Fast Fourier Transform array (yf) and the corresponding frequncy values (xf) of the sampled signal.
    If plot == True, plots the frequency domain plot, and num_duplicates duplicates of the frequency.
    """
    n = len(x_sampled)
    yf = fft(x_sampled) #the fast fourier transform of the sampled signal (magnitude and phase, complex number)
    xf = fftfreq(n, 1 / sampling_freq) #the corresponding frequencies of the sampled signal

    if plot == True:
        magnitude = np.abs(yf) #the modulus of the fourier transform of the sampled signal, in order to access the magnitude
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
        plt.figure(figsize=(15, 5.5))
        plt.plot(xf_tiled, magnitude_tiled, color = "black")
        plt.title(f"Frequency Domain Representation of {sampling_freq}Hz Sampled Signal", size = 30)
        plt.xlabel("Frequency (Hertz)", size = 20)
        plt.grid(True, which = "both", linestyle = "--", linewidth = 0.5)
        plt.axvline(x=0, color='gray', linestyle='--', linewidth=1)
        plt.ylabel("Magnitude", size = 20)
       
        #for axis ticks of multiples of 2
        x_min, x_max = plt.xlim()
        tick_start = np.ceil(x_min / 2) * 2 
        tick_end = np.floor(x_max / 2) * 2 
        plt.xticks(np.arange(tick_start, tick_end + 1, 2), size = 10) #size parameter to control for font size
        plt.axvline(x=sampling_freq / 2, color='#FF00FF', linestyle='--', linewidth=2) #green vertical line at fs/2 and -fs/2
        plt.axvline(x=-sampling_freq / 2, color='#FF00FF', linestyle='--', linewidth=2)

        plt.show()

    return yf, xf


#4: RECONSTRUCTION
#We now reconstruct the original signal from the sampled signal.
#the signal can be recovered applying an (ideal band pass) filter --> in time domain this looks like the sinc function
#we do this in the time domain in order to avoid circular convolution
#if we had done a multiplication in the frequency domain instead, we would have had to zero pad the signal to avoid circular convolution
def reconstruction(x_sampled, t_sampled, plot = False, x_continuous = None, t_s = None):
    """
    Returns the reconstructed signal from the sampled signal x_sampled, using t_sampled (the discrete timesteps of the sampled signal) and t_s (the time axis that we want the signal to be reconstructed on).
    If plot = True, plots the reconstructed signal along with the original signal and sampled points.
    """

    Fs = 1/(t_sampled[1] - t_sampled[0]) #calculates the sampling frequency

    x_s = np.zeros(len(t_s)) #initializing the reconstructed signal array
    for n in range(0, len(t_sampled)): #we loop through the sampled signal, this is a finite sum
        x_s = x_s + x_sampled[n] * np.sinc(Fs * t_s - n) #this is the filter (in the time domain) that reconstructs the original signal from the sampled signal.
    
    if plot == True:
        plt.figure(figsize=(12, 6))
        plt.plot(t_s, x_continuous, label = "Original", alpha = 0.9, lw = 2)
        plt.plot(t_s, x_s, label = "Reconstructed", lw = 2, ls = "--", color = "red")
        plt.title(f"Reconstructed Signal (sampling frequency {sampling_frequency} Hz)", size = 30)
        plt.xlabel("Time", size = 20)
        plt.ylabel("Amplitude", size = 20)
        plt.legend(loc="upper left")
        plt.show()

    return x_s

if __name__ == "__main__":

    t_continuous, x_continuous = generate_signal(t_end, frequency, signal_type = signal_type, plot = False)
    print(f"len(x_continuous) = {len(x_continuous)}") 

    t_sampled, x_sampled = sample_signal(x_continuous, t_continuous, sampling_frequency, plot_one = False, plot_two = False, plot_three = False)

    yf, xf = sampled_fourier_transform(x_sampled, sampling_frequency, num_duplicates = 2, plot = True)

    x_s = reconstruction(x_sampled, t_sampled, plot = True, x_continuous=x_continuous, t_s=t_continuous)

