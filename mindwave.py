import numpy as np
import pandas as pd
import sys
import json
import time
from telnetlib import Telnet

# Initializing lists required to store the data.
attention_values = []
meditation_values = []
delta_values = []
theta_values = []
lowAlpha_values = []
highAlpha_values = []
lowBeta_values = []
highBeta_values = []
lowGamma_values = []
highGamma_values = []
blinkStrength_values = []
time_array = []

# Establish a connection to the EEG device
try:
    tn = Telnet('localhost', 13854)
except Exception as e:
    print(f"Error connecting to the Telnet server: {e}")
    sys.exit(1)

start = time.perf_counter()

tn.write(b'{"enableRawOutput": true, "format": "Json"}\r\n')

outfile = None
if len(sys.argv) > 1:
    outfile = sys.argv[-1]
    outfptr = open(outfile, 'w')

eSenseDict = {'attention': 0, 'meditation': 0}
waveDict = {'lowGamma': 0, 'highGamma': 0, 'highAlpha': 0, 'delta': 0, 'highBeta': 0, 'lowAlpha': 0, 'lowBeta': 0, 'theta': 0}
signalLevel = 0

# Capture data for 30 seconds
while time.perf_counter() - start < 60:
    blinkStrength = 0
    line = tn.read_until(b'\r').decode('utf-8').strip()
    if len(line) > 20:
        timediff = time.perf_counter() - start
        data_dict = json.loads(line)
        signalLevel = data_dict.get('poorSignalLevel', 0)
        blinkStrength = data_dict.get('blinkStrength', 0)
        if "eegPower" in data_dict:
            waveDict = data_dict['eegPower']
            eSenseDict = data_dict['eSense']
        
        # Append values to lists
        time_array.append(timediff)
        blinkStrength_values.append(blinkStrength)
        lowGamma_values.append(waveDict['lowGamma'])
        highGamma_values.append(waveDict['highGamma'])
        highAlpha_values.append(waveDict['highAlpha'])
        delta_values.append(waveDict['delta'])
        lowBeta_values.append(waveDict['lowBeta'])
        highBeta_values.append(waveDict['highBeta'])
        theta_values.append(waveDict['theta'])
        lowAlpha_values.append(waveDict['lowAlpha'])
        attention_values.append(eSenseDict['attention'])
        meditation_values.append(eSenseDict['meditation'])

        # Output string for logging or debugging
        outputstr = f"{timediff}, {signalLevel}, {blinkStrength}, {eSenseDict['attention']}, {eSenseDict['meditation']}, {waveDict['lowGamma']}, {waveDict['highGamma']}, {waveDict['highAlpha']}, {waveDict['delta']}, {waveDict['highBeta']}, {waveDict['lowAlpha']}, {waveDict['lowBeta']}, {waveDict['theta']}"
        print(outputstr)
        if outfile:
            outfptr.write(outputstr + "\n")

# Gather metadata from user input
person_name = input('Enter the name of the person: ')

lefty_righty = input('Is the person left-handed or right-handed: ')


# Create a DataFrame for the new data with each timestamp as a separate row
data = pd.DataFrame({
    'Name': [person_name] * len(time_array),
    'time': time_array,
    'attention': attention_values,
    'meditation': meditation_values,
    'delta': delta_values,
    'theta': theta_values,
    'lowAlpha': lowAlpha_values,
    'highAlpha': highAlpha_values,
    'lowBeta': lowBeta_values,
    'highBeta': highBeta_values,
    'lowGamma': lowGamma_values,
    'highGamma': highGamma_values,
    'blinkStrength': blinkStrength_values,
    # 'LOR': [blink_label] * len(time_array),
    #'time_start': [time_starting] * len(time_array),
    'LTYRTY': [lefty_righty] * len(time_array),
    # 'time_blink': [time_blinking] * len(time_array)
})

name = input("Name Of the File: ")
name += ".csv"
# Reading the data stored till now
try:
    dataset = pd.read_csv(name)
    dataset = pd.concat([dataset, data], ignore_index=True)
except FileNotFoundError:
    dataset = data

# Save the updated dataset with separate rows for each time point
dataset.to_csv(name, index=False)

# Close Telnet and file connections
tn.close()
if outfile:
    outfptr.close()
