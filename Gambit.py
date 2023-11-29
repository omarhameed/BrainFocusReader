import time as datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from bitalino import BITalino
import numpy as np


# The macAddress variable on Windows can be "XX:XX:XX:XX:XX:XX" or "COMX"
# while on Mac OS can be "/dev/tty.BITalino-XX-XX-DevB" for devices ending with the last 4 digits of the MAC address or "/dev/tty.BITalino-DevB" for the remaining
macAddress = "EC:1B:BD:62:F4:D9"

# This example will collect data for 5 sec.
running_time = 5
'''
    - running_time: Duration of data acquisition in seconds.
    - batteryThreshold: Sets the battery threshold.
    - acqChannels: Specifies the channels to be used for data acquisition.
    - samplingRate: Defines the sampling rate in Hz.
    - nSamples: Number of samples to be read in each iteration.
        digitalOutput_on and digitalOutput_off: Used to control digital outputs like 
        LED and buzzer on the BITalino.
'''
batteryThreshold = 30
acqChannels = [0, 1, 2, 3, 4, 5]
samplingRate = 1000
nSamples = 5
digitalOutput_on = [1, 1]
digitalOutput_off = [0, 0]

#  establishes a connection to the device using the provided MAC address.
device = BITalino(macAddress)

# Set battery threshold
device.battery(batteryThreshold)

# Prints the firmware version of the BITalino.
print(device.version())

'''
# Begins the data acquisition process with the specified sampling rate and channels.

 - configuring and starting data acquisition on a device with specified parameters 
    (sampling rate and analog channels). 
 - The function's success is implicit if it completes without raising any exceptions. 
 - If the function encounters any issues (like an invalid sampling rate or analog channel configuration), 
    it raises an exception, and the normal flow of the function is interrupted.

'''
device.start(samplingRate, acqChannels)


start = time.time()
end = time.time()
time_taken = datetime.now()
dt_string = time_taken.strftime("%d_%m_%Y__%H_%M_%S")

header = ["Sequence Number", "Digital 1", "Digital 2", "Digital 3", "Digital 4", "Analog 1", "Analog 2", "Analog 3", "Analog 4","Analog 5","Analog 6"]

# Create the file and write the header
with open(f"{dt_string}.csv", 'w', newline='') as file:
    np.savetxt(file, [header], delimiter=",", fmt='%s')

i = 1
# This loop continues for the duration defined by running_time. In each iteration, it reads nSamples from the BITalino and prints them.
with open(f"{dt_string}.csv", 'a', newline='') as wr:
    while (end - start) < running_time:
        # Read samples
        
        samples = device.read(nSamples)
        #print(samples)  # Print the samples
        np.savetxt(wr, samples, delimiter=",")  # Append data to CSV
        end = time.time()
        print(i)
        i = i+1

# Stop acquisition and close connection
device.trigger(digitalOutput_off)
device.stop()
device.close()


# Setup the plot
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r-', animated=True)

# Initialize the plot frame
def init():
    ax.set_xlim(0, 100)
    ax.set_ylim(-1, 1)  # Adjust the y limits according to the expected amplitude of your signals
    return ln,

# Update function for animation
def update(frame):
    global device, nSamples
    samples = device.read(nSamples)
    y = samples[:, -1]  # Assuming we're interested in the last channel (-1 for Analog 6)
    x = frame * nSamples + np.arange(nSamples)
    xdata.extend(x)
    ydata.extend(y)
    ln.set_data(xdata, ydata)
    ax.set_xlim(x[0], x[-1] + 100)
    return ln,

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=range(100),
                              init_func=init, blit=True)

# Show the plot
plt.show()

# Stop acquisition and close connection (this should be executed when the animation is closed)
device.stop()
device.close()
