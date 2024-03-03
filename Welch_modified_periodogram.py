import pandas as pd
import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('Analog4_O2_on_our_dev/SignalData.csv')  # Adjust the path as necessary

# Extract specific columns
sequence_numbers = df['Sequence Number n']  # Adjust column name as necessary
eeg_values = df['EEG (V)']  # Adjust column name as necessary

# Use Welch's method to compute the power spectral density
frequencies, psd_values = welch(eeg_values, 500, window='hann', nperseg=2000, noverlap=None)

# Filter frequencies and PSD values to only include frequencies in the range 0 to 40 Hz
mask = (frequencies >= 0) & (frequencies <= 40)
filtered_frequencies = frequencies[mask]
filtered_psd_values = psd_values[mask]

# Plot the filtered power spectral density
plt.semilogy(filtered_frequencies, filtered_psd_values)
plt.title('Welch Periodogram')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power/Frequency [V^2/Hz]')
plt.xlim(0, 40)  # This ensures that the x-axis only shows the range from 0 to 40 Hz
plt.show()
