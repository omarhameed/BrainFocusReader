import time
import csv
import numpy as np
from bitalino import BITalino
from datetime import datetime


# The macAddress variable on Windows can be "XX:XX:XX:XX:XX:XX" or "COMX"
# while on Mac OS can be "/dev/tty.BITalino-XX-XX-DevB" for devices ending with the last 4 digits of the MAC address or "/dev/tty.BITalino-DevB" for the remaining
macAddress = "EC:1B:BD:62:F4:D9"

# This example will collect data for 5 sec.
running_time = 5

batteryThreshold = 30
acqChannels = [0, 1, 2, 3, 4, 5]
samplingRate = 1000
nSamples = 50
digitalOutput_on = [1, 1]
digitalOutput_off = [0, 0]

# Connect to BITalino
device = BITalino(macAddress)

# Set battery threshold
device.battery(batteryThreshold)

# Read BITalino version
print(device.version())

# Start Acquisition
device.start(samplingRate, acqChannels)

start = time.time()
end = time.time()
time_taken = datetime.now()
dt_string = time_taken.strftime("%d_%m_%Y__%H_%M_%S")

header = ["Sequence Number", "Digital 0", "Digital 1", "Digital 2", "Digital 3", "Analog 0", "Analog 1", "Analog 2", "Analog 3"]

# Create the file and write the header
with open(f"{dt_string}.csv", 'w', newline='') as file:
    np.savetxt(file, [header], delimiter=",", fmt='%s')

with open(f"{dt_string}.csv", 'a', newline='') as wr:
    while (end - start) < running_time:
        # Read samples
        samples = device.read(nSamples)
        print(samples)  # Print the samples
        np.savetxt(wr, samples, delimiter=",")  # Append data to CSV
        end = time.time()

# Stop acquisition and close connection
device.trigger(digitalOutput_off)
device.stop()
device.close()
