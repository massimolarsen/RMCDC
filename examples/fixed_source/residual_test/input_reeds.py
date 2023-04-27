import numpy as np
import h5py
import sys
sys.path.append('C:/users/larse/source/repos/RMCDC')
import mcdc

# =============================================================================
# Set model
# =============================================================================

X = 6.0

# Set materials
m1 = mcdc.material(
    capture=np.array([0.1]),
    scatter=np.array([[0.9]])
)

m2 = mcdc.material(
    capture=np.array([0])
)

m3 = mcdc.material(
    capture=np.array([5.0])
)

m4 = mcdc.material(
    capture=np.array([50.0])
)

# Set surfaces
s1 = mcdc.surface("plane-z", z=0, bc="vacuum")
s2 = mcdc.surface("plane-z", z=2.0)
s3 = mcdc.surface("plane-z", z=4.0)
s4 = mcdc.surface("plane-z", z=5.0)
s5 = mcdc.surface("plane-z", z=6.0)
s6 = mcdc.surface("plane-z", z=8.0, bc="reflective")

# Set cells
mcdc.cell([+s1, -s2], m1)
mcdc.cell([+s2, -s3], m1)
mcdc.cell([+s3, -s4], m2)
mcdc.cell([+s4, -s5], m3)
mcdc.cell([+s5, -s6], m4)

# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

Nz = 80
Nmu = 2

# Tally: cell-average and cell-edge angular fluxes and currents
mcdc.tally(
    scores=["flux"],
    z=np.linspace(0.0, 8.0, Nz + 1),
    mu=np.linspace(-1.0, 1.0, Nmu + 1)
)

# =============================================================================
# Residual Parameters
# =============================================================================

hi = 8.0 / Nz
hj = 2.0 / Nmu

estimate = np.ones([Nz, Nmu]) * 0

#estimate = np.array([[6,0],[6,0],[6,0]])


#with h5py.File("rmc1e6noestimate.h5", "r") as f:
    #estimate = f["tally/flux/mean"][:]

#with h5py.File("output.h5", "r") as f:
    #estimate = f["tally/flux/mean"][:]

#fixed_source = np.zeros([Nx, Nmu]) * Nx * Nmu
#fixed_source[0,0] = Nx*Nmu
#fixed_source[0,1] = Nx*Nmu

fixed_source = np.ones([Nz, Nmu]) * 0

for i in range(20):
    fixed_source[i+20,:] = 1/2
    fixed_source[i+60,:] = 50/2

#fixed_source = np.ones([Nz, Nmu]) * 1

interior_integral = np.zeros_like(fixed_source)
face_integral = np.zeros_like(fixed_source)
interior_residual = np.zeros_like(fixed_source)
face_residual = np.zeros_like(fixed_source)
residual_norm = np.zeros_like(fixed_source)

exponential_convergence = True

mcdc.residual(
    hi=hi,
    hj=hj,
    estimate=estimate,
    fixed_source=fixed_source,
    interior_integral=interior_integral,
    face_integral=face_integral,
    interior_residual=interior_residual,
    face_residual=face_residual,
    residual_norm=residual_norm,
    exponential_convergence=exponential_convergence
)

# Setting
mcdc.setting(N_particle=1e5)

# Run
mcdc.run()