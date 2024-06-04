import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

num_samples=200
dt = 0.001
f=50
theta_in = 25*np.pi/180
theta_out = -20*np.pi/180
n = np.arange(num_samples) # Number of points

 # Create input and output signals
x = 3*np.cos(2*np.pi*f*n*dt+theta_in)
y = 1.5*np.cos(2*np.pi*f*n*dt+theta_out)

# Create Hilbert transforms of signals
X = hilbert(x)
Y = hilbert(y)

# Get magnitude and phases of Hilbert transforms
X_mag = np.abs(X)
X_phase = np.angle(X, deg=True)
H = np.divide(Y,X)
H_mag = np.abs(H)
H_phase = np.angle(H,deg=True)

 # Plot results
plt.figure()
plt.plot(n*dt, x, label='Original')
plt.plot(n*dt, X_mag,'r',label='Hilbert')
plt.xlabel('Time (s)')
plt.ylabel('Value')
plt.legend()

plt.figure()
plt.plot(n*dt,H_mag)
plt.ylim([0,1])
plt.xlabel('Time (s)')
plt.ylabel('Magnitdue')
plt.title('Gain')
plt.figure()
plt.plot(n*dt,H_phase)
plt.ylim([-90,90])
plt.xlabel('Time (s)')
plt.ylabel('Phase(Deg)')
plt.title('Phase')
plt.show()

