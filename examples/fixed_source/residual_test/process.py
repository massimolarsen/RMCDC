import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import h5py

# =============================================================================
# Reference solution (SS)
# =============================================================================

# Load grids
with h5py.File("output.h5", "r") as f:
    x = f["tally/grid/x"][:]
    t = f["tally/grid/t"][:]

dx = x[1] - x[0]
x_mid = 0.5 * (x[:-1] + x[1:])
dt = t[1:] - t[:-1]
K = len(dt)
J = len(x_mid)


# =============================================================================
# Animate results
# =============================================================================

with h5py.File("output.h5", "r") as f:
    phi = f["tally/flux/mean"][:]
    phi_sd = f["tally/flux/sdev"][:]

with h5py.File("rmc1e6estimate.h5", "r") as f:
    phi1 = f["tally/flux/mean"][:]
with h5py.File("rmc1e6noestimate.h5", "r") as f:
    phi2 = f["tally/flux/mean"][:]
with h5py.File("outputtest.h5", "r") as h:
    phi3 = h["tally/flux/mean"][:]

print(phi)
phi = np.sum(phi, axis=1)
#print(phi1)
phi1 = np.sum(phi1, axis=1)
#print(phi2)
phi2 = np.sum(phi2, axis=1)

phi3 = np.sum(phi3, axis=1)
#print(phi3)

x= np.linspace(0,1,2)

#plt.plot(x, phi, label="RMC with no estimate")
plt.step(x, phi, where="mid", label="RMC with estimate") 


#plt.step(x, phi1, where="mid", label="RMC with estimate") 
#plt.step(x, phi2, where="mid", label="RMC with no estimate")
#plt.step(x, phi3, where="mid", label="Standard MC")


#plt.plot(x, phi2, label="RMC with no estimate")
#plt.plot(x, phi3, label="Standard MC")
plt.title("1e6 particles, constant source, vacuum boundary, 1/100 scattering")
plt.xlabel("x")
plt.ylabel("flux")
plt.legend()


plt.show()
