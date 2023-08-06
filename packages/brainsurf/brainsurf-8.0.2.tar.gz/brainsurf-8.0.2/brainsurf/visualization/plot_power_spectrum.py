import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def plot_power_spectrum_fft(data, sfreq):
    """
    Compute and plot the power spectrum of EEG data.
    
    Parameters
    ----------
    data : array-like, shape (n_channels, n_samples)
        The EEG data.
    sfreq : float
        The sampling frequency of the data, in Hz.
    """
    n_channels, n_samples = data.shape
  
    freqs = np.fft.rfftfreq(n_samples, 1/sfreq)

    psd = np.abs(np.fft.rfft(data, axis=1))**2 / (n_samples * sfreq)
    
    fig, ax = plt.subplots()
    for i in range(n_channels):
        ax.plot(freqs, psd[i], label=f'Channel {i+1}')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power ($\mu V^2$/Hz)')
    ax.legend()
    plt.show()


def welch_power_spectrum(freqs, psd, nperseg=1024):
    plt.figure()
    plt.plot(freqs, psd)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSD')
    plt.title('Frequency-Domain EEG Signal')
    plt.show()
    

import matplotlib.pyplot as plt

def visualize_difference_plot(overlapping_df1, overlapping_df2):
    """
    Visualize the difference in overlapping percentage between two conditions/time points using a bar plot.

    Args:
    - overlapping_df1 (pandas.DataFrame): DataFrame containing the overlapping percentage values for condition/time point 1.
    - overlapping_df2 (pandas.DataFrame): DataFrame containing the overlapping percentage values for condition/time point 2.
    
    Returns:
    - None (displays the bar plot)
    """
    difference_df = overlapping_df1 - overlapping_df2

    # Calculate the mean difference for each frequency band
    mean_difference = difference_df.mean()
    
    # Plotting the mean difference
    plt.figure(figsize=(10, 6))
    mean_difference.plot(kind='bar')

    plt.xlabel('Frequency Bands')
    plt.ylabel('Difference in Overlapping Percentage')
    plt.title('Difference in Overlapping Percentage between Conditions/Time Points')
    plt.xticks(rotation=45)
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

def calculate_band_powers(data, sampling_rate):
    bands = {'Delta': (0.5, 4),
             'Theta': (4, 8),
             'Alpha': (8, 13),
             'Beta': (13, 30)}
    
    band_powers = {}
    for column in data.columns:
        freqs, psd = welch(data[column], fs=sampling_rate)
        channel_band_powers = {}
        for band_name, (fmin, fmax) in bands.items():
            indices = np.where((freqs >= fmin) & (freqs < fmax))
            band_power = np.trapz(psd[indices], freqs[indices])
            channel_band_powers[band_name] = band_power
        band_powers[column] = channel_band_powers
    
    return band_powers

def compare_power(pre_data, post_data, sampling_rate):
    pre_data = pre_data.iloc[:, :10]  # Select first 10 channels
    post_data = post_data.iloc[:, :10]  # Select first 10 channels
    
    pre_band_powers = calculate_band_powers(pre_data, sampling_rate)
    post_band_powers = calculate_band_powers(post_data, sampling_rate)
    
    channels = list(pre_band_powers.keys())
    bands = list(pre_band_powers[channels[0]].keys())
    pre_powers = np.array([list(band_powers.values()) for band_powers in pre_band_powers.values()])
    post_powers = np.array([list(band_powers.values()) for band_powers in post_band_powers.values()])
    
    num_channels = len(channels)
    num_bands = len(bands)
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.arange(num_channels)
    rects1 = ax.bar(x - width/2, pre_powers.mean(axis=1), width, label='Pre-Meditation')
    rects2 = ax.bar(x + width/2, post_powers.mean(axis=1), width, label='Post-Meditation')
    ax.set_xlabel('Channels')
    ax.set_ylabel('Power')
    ax.set_title('Power Comparison between Pre and Post-Meditation (First 10 Channels)')
    ax.set_xticks(x)
    ax.set_xticklabels(channels)
    ax.legend()
    
    for rect in rects1 + rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

def compare_power_bands(pre_data, post_data, sampling_rate):
    pre_data = pre_data.iloc[:, :10]  # Select first 10 channels
    post_data = post_data.iloc[:, :10]  # Select first 10 channels

    pre_band_powers = calculate_band_powers(pre_data, sampling_rate)
    post_band_powers = calculate_band_powers(post_data, sampling_rate)

    channels = list(pre_band_powers.keys())
    bands = list(pre_band_powers[channels[0]].keys())

    pre_powers = np.array([list(band_powers.values()) for band_powers in pre_band_powers.values()])
    post_powers = np.array([list(band_powers.values()) for band_powers in post_band_powers.values()])

    diff_powers = post_powers - pre_powers

    num_channels = len(channels)
    width = 0.2
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(num_channels)

    rects1 = ax.bar(x - width, diff_powers[:, 0], width, label='Delta')
    rects2 = ax.bar(x, diff_powers[:, 1], width, label='Theta')
    rects3 = ax.bar(x + width, diff_powers[:, 2], width, label='Alpha')
    rects4 = ax.bar(x + 2 * width, diff_powers[:, 3], width, label='Beta')

    ax.set_xlabel('Channels')
    ax.set_ylabel('Power Difference')
    ax.set_title('Power Difference between Pre and Post-Meditation (First 10 Channels)')
    ax.set_xticks(x)
    ax.set_xticklabels(channels)
    ax.legend()

    plt.tight_layout()
    plt.show()