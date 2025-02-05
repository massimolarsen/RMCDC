import matplotlib.pyplot as plt
import h5py
import numpy as np

from reference import reference


# Load results
with h5py.File("output.h5", "r") as f:
    z = f["tally/grid/z"][:]
    dz = z[1:] - z[:-1]
    z_mid = 0.5 * (z[:-1] + z[1:])

    mu = f["tally/grid/mu"][:]
    dmu = mu[1:] - mu[:-1]
    mu_mid = 0.5 * (mu[:-1] + mu[1:])

    psi = f["tally/flux/mean"][:]
    psi_sd = f["tally/flux/sdev"][:]
    psi_z = f["tally/flux-z/mean"][:]
    psi_z_sd = f["tally/flux-z/sdev"][:]
    J = f["tally/current/mean"][:, 2]
    J_sd = f["tally/current/sdev"][:, 2]
    J_z = f["tally/current-z/mean"][:, 2]
    J_z_sd = f["tally/current-z/sdev"][:, 2]

I = len(z) - 1
N = len(mu) - 1

# Scalar flux
phi = np.zeros(I)
phi_sd = np.zeros(I)
phi_z = np.zeros(I + 1)
phi_z_sd = np.zeros(I + 1)
for i in range(I):
    phi[i] += np.sum(psi[i, :])
    phi_sd[i] += np.linalg.norm(psi_sd[i, :])
    phi_z[i] += np.sum(psi_z[i, :])
    phi_z_sd[i] += np.linalg.norm(psi_z_sd[i, :])
phi_z[I] += np.sum(psi_z[I, :])
phi_z_sd[I] += np.linalg.norm(psi_z_sd[I, :])

# Normalize
phi /= dz
phi_sd /= dz
J /= dz
J_sd /= dz
for n in range(N):
    psi[:, n] = psi[:, n] / dz / dmu[n]
    psi_sd[:, n] = psi_sd[:, n] / dz / dmu[n]

# Reference solution
phi_ref, phi_z_ref, J_ref, J_z_ref, psi_ref, psi_z_ref = reference(z, mu)

# Flux - spatial average
plt.plot(z_mid, phi, "-b", label="MC")
plt.fill_between(z_mid, phi - phi_sd, phi + phi_sd, alpha=0.2, color="b")
plt.plot(z_mid, phi_ref, "--r", label="Ref.")
plt.xlabel(r"$z$, cm")
plt.ylabel("Flux")
plt.ylim([0.06, 0.16])
plt.grid()
plt.legend()
plt.title(r"$\bar{\phi}_i$")
plt.show()

# Flux - spatial grid
plt.plot(z, phi_z, "-b", label="MC")
plt.fill_between(z, phi_z - phi_z_sd, phi_z + phi_z_sd, alpha=0.2, color="b")
plt.plot(z, phi_z_ref, "--r", label="Ref.")
plt.xlabel(r"$z$, cm")
plt.ylabel("Flux")
plt.ylim([0.06, 0.16])
plt.grid()
plt.legend()
plt.title(r"$\phi(z)$")
plt.show()

# Current - spatial average
plt.plot(z_mid, J, "-b", label="MC")
plt.fill_between(z_mid, J - J_sd, J + J_sd, alpha=0.2, color="b")
plt.plot(z_mid, J_ref, "--r", label="Ref.")
plt.xlabel(r"$z$, cm")
plt.ylabel("Current")
plt.ylim([-0.03, 0.045])
plt.grid()
plt.legend()
plt.title(r"$\bar{J}_i$")
plt.show()

# Current - spatial grid
plt.plot(z, J_z, "-b", label="MC")
plt.fill_between(z, J_z - J_z_sd, J_z + J_z_sd, alpha=0.2, color="b")
plt.plot(z, J_z_ref, "--r", label="Ref.")
plt.xlabel(r"$z$, cm")
plt.ylabel("Current")
plt.ylim([-0.03, 0.045])
plt.grid()
plt.legend()
plt.title(r"$J(z)$")
plt.show()

# Angular flux - spatial average
vmin = min(np.min(psi_ref), np.min(psi))
vmax = max(np.max(psi_ref), np.max(psi))
fig, ax = plt.subplots(1, 2, sharey=True)
Z, MU = np.meshgrid(z_mid, mu_mid)
im = ax[0].pcolormesh(MU.T, Z.T, psi_ref, vmin=vmin, vmax=vmax)
ax[0].set_xlabel(r"Polar cosine, $\mu$")
ax[0].set_ylabel(r"$z$")
ax[0].set_title(r"\psi")
ax[0].set_title(r"$\bar{\psi}_i(\mu)$ [Ref.]")
ax[1].pcolormesh(MU.T, Z.T, psi, vmin=vmin, vmax=vmax)
ax[1].set_xlabel(r"Polar cosine, $\mu$")
ax[1].set_ylabel(r"$z$")
ax[1].set_title(r"$\bar{\psi}_i(\mu)$ [MC]")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label("Angular flux")
plt.show()
