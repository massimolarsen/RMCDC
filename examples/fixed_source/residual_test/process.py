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
    print(phi)
    phi_sd = f["tally/flux/sdev"][:]
    phi_x = f["tally/flux-x/mean"][:]
    phi_x_sd = f["tally/flux-x/sdev"][:]

phi = np.sum(phi, axis=1)


plt.plot(phi)

# Flux - average
fig = plt.figure()
ax = plt.axes(
    xlim=(0, 1), ylim=(0, 2)
)
ax.grid()
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"Flux")
ax.set_title(r"$\bar{\phi}_{k,j}$")
(line1,) = ax.plot([], [], "-b", label="MC")
(line2,) = ax.plot([], [], "--r", label="Ref.")
text = ax.text(0.02, 0.9, "", transform=ax.transAxes)
ax.legend()

plt.show()

# Flux - x
fig = plt.figure()
ax = plt.axes(
    xlim=(0, 1), ylim=(0, 2)
)
ax.grid()
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"Flux")
ax.set_title(r"$\bar{\phi}_{k}(x)$")
(line1,) = ax.plot([], [], "-b", label="MC")
(line2,) = ax.plot([], [], "--r", label="Ref.")
text = ax.text(0.02, 0.9, "", transform=ax.transAxes)
ax.legend()

plt.show()
