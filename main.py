# LED I-V Characteristic Curve Tracer

import pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt
from tme import device_addresses

# Define lists for parameters
colors = ['Red','Yellow','Green','Blue','White']
col = ['R','Y','G','B','W']
linecolors = ['r','y','g','b','k']
image_name = 'LED_IV_Curves.png'
file_name = 'LED_IV_Curves.txt'
ps_Vmax = 10 # Maximum power supply voltage
num_points = 100 # Number of points per sweep
R = 330 # Resistor Value (Ohms)
ps_voltages = np.linspace(0,ps_Vmax,num_points).tolist()

# Initialize lists
fheader = ''
data = np.zeros([num_points,3*len(colors)])

# Get the addresses for the equipment and open the resource manager
devices = device_addresses()
print(devices)
rm = visa.ResourceManager()

# Set up the objects representing the equipment
ps = rm.open_resource(devices.ps_address)
ps.read_termination = '\n'
ps.write_termination = '\n'

# Set the power supply channel to initial settings
ps.write('OUTP 0,(@2)')
ps.write('APPL P25V,0,1') # Sets Channel 2 to 0 Volts, 1 Amp limit
ps.write('OUTP 1,(@2)')
ps.query('*OPC?')

# Loop over the different LED colors
for i in range(len(colors)):
    ps.write('OUTP 0,(@2)')
    c = col[i]
    fheader = fheader + 'V_PS_' + c + ',V_LED_' + c + ',I_' + c + ','
    inp = input('Place the {} LED in the circuit and press ENTER'\
                .format(colors[i]))
    ps.write('OUTP 1,(@2)')
    ps.query('*OPC?')
    for k in range(num_points):
        voltage = ps_voltages[k]
        print('Applying {a:3.2f} Volts to {b} circuit'\
              .format(a=voltage,b=colors[i]))
        ps.write('VOLT {}, (@2)'.format(voltage))
        ps.query('*OPC?')
        time.sleep(1)
        # TODO: Still need PS, but need to change PS to DMM for reading voltage and current
        Vps = float(ps.query('MEAS:VOLT? (@2)')) # Power Supply Voltage
        Ips = float(ps.query('MEAS:CURR? (@2)')) # Power Supply Current
        ps.query('*OPC?')
        V_led = Vps-Ips*R
        data[k,i*3] = Vps
        data[k,i*3+1] = V_led
        data[k,i*3+2] = Ips
        Ips = Ips*1000 # Convert to mA
    ps.write('VOLT 0,(@2)')

fheader = fheader.rstrip(fheader[-1]) # Strip last comma from header

# Plot the results
plt.figure()
for i in range(len(colors)):
    plt.plot(data[:,i*3+1],data[:,i*3+2]*1000,linecolors[i]\
             ,label=colors[i])
    
plt.legend() 
plt.grid()
plt.xlabel('Forward Voltage (V)')
plt.ylabel('Current (mA)')
plt.title('LED I-V Analysis')   
plt.savefig(image_name) # Save figure
plt.show()

# Save data to file
np.savetxt(file_name, data, fmt='%0.3f', delimiter=',', header=fheader)