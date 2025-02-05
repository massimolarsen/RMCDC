from plotter import plot_convergence
from reference import reference
import numpy as np
import h5py
import sys

sys.path.append("../../util")


N_min = int(sys.argv[1])
N_max = int(sys.argv[2])
N_particle_list = np.logspace(N_min, N_max, (N_max - N_min) * 2 + 1)

# Reference solution
phi_ref = reference()

error = []

for N_particle in N_particle_list:
    # Get results
    with h5py.File("output_%i.h5" % int(N_particle), "r") as f:
        phi = f["tally/flux/mean"][:]

    error.append(np.linalg.norm((phi - phi_ref) / phi_ref))

plot_convergence("inf_casmo70_flux", N_particle_list, error)
