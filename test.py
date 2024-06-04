import pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt
from tme import device_addresses
from power_supply_library import power_supply
from dmm import dmm
from waveform import wave
from scope import scope


devices = device_addresses()
rm=visa.ResourceManager()
wave_add = devices.wfg_address
wave = wave(rm, wave_add)
scope_add = devices.scope_address
scope = scope(rm, scope_add)

wave.connect()
scope.connect()
# Automated Replacement
wave.high_z()
wave.square_wave()
wave.output(1)
scope.channel("on", 2)
scope.channel("on", 1)
scope.run()
scope.autoscale()
# Burst Section
time.sleep(5)
wave.output(0)
wave.burst_characteristics()
scope.single()
wave.trigger()
wave.output(1)
#                 PLOTTING SECTION
import matplotlib.pyplot as plt

times1, volts1 = scope.get_waveform_binary()
times2, volts2 = scope.get_waveform_ascii(channel=2)

fig, ax = plt.subplots()
ax.plot(times2, volts2, label='VC')
ax.plot(times1, volts1, label='Vin')
ax.set_ylabel('Voltage')
ax.set_xlabel('Time')
ax.set_title('Pulse Wave')
ax.legend()  # Add a legend based on the labels

plt.savefig("Test.jpg")
plt.show()

fig, ax = plt.subplots()
ax.plot(times2, volts2, label='VC')
ax.plot(times2, volts2, 'k:', label='Estimation')  # Dotted line for VC curve
plt.savefig("CurveFit.jpg")
plt.show()



scope.screen_capture()