import numpy as np
import h5py
import sys
sys.path.append('C:/users/larse/source/repos/RMCDC')
import mcdc

# =============================================================================
# Set model
# =============================================================================

# Set materials
m1 = mcdc.material(
    capture=np.array([1.0])
)

m2 = mcdc.material(
    capture=np.array([9.0/10.0]),
    scatter=np.array([[1.0/10.0]])
)

# Set surfaces
s1 = mcdc.surface("plane-z", z=0.0, bc="vacuum")
s2 = mcdc.surface("plane-z", z=1.0, bc="vacuum")
#s3 = mcdc.surface("plane-x", x=2.0, bc="vacuum")

# Set cells
mcdc.cell([+s1, -s2], m1)
#mcdc.cell([+s2, -s3], m2)

# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

Nz = 2
Nmu = 2

# Tally: cell-average and cell-edge angular fluxes and currents
mcdc.tally(
    scores=["flux"],
    z=np.linspace(0.0, 1.0, Nz + 1),
    mu=np.linspace(-1.0, 1.0, Nmu + 1)
)

# =============================================================================
# Residual Parameters
# =============================================================================

hi = 1.0 / Nz
hj = 2.0 / Nmu
#estimate = np.zeros([Nz, Nmu])

estimate = np.ones([Nz, Nmu]) * 6

#estimate = np.array([[5,2],[10, 20]])


#with h5py.File("rmc1e6noestimate.h5", "r") as f:
    #estimate = f["tally/flux/mean"][:]

#with h5py.File("output.h5", "r") as f:
    #estimate = f["tally/flux/mean"][:]

#fixed_source = np.zeros([Nx, Nmu]) * Nx * Nmu
#fixed_source[0,0] = Nx*Nmu
#fixed_source[0,1] = Nx*Nmu
fixed_source = np.ones([Nz, Nmu]) * 5

interior_integral = np.zeros_like(fixed_source)
face_integral = np.zeros_like(fixed_source)
interior_residual = np.zeros_like(fixed_source)
face_residual = np.zeros_like(fixed_source)
residual_source = np.zeros_like(fixed_source)

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
    residual_source=residual_source,
    exponential_convergence=exponential_convergence
)

# Setting
mcdc.setting(N_particle=1e4)

# Run
mcdc.run()