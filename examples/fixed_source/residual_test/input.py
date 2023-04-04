import numpy as np
import h5py
import sys
sys.path.append('C:/users/larse/source/repos/RMCDC')
import mcdc

# =============================================================================
# Set model
# =============================================================================
# Infinite medium with isotropic plane surface at the center
# Based on Ganapol LA-UR-01-1854 (AZURV1 benchmark)
# Effective scattering ratio c = 1.1

# Set materials
m1 = mcdc.material(
    capture=np.array([100.0/100.0]),
    scatter=np.array([[0.0/100.0]])
)

m2 = mcdc.material(
    capture=np.array([10.0/10.0]),
    scatter=np.array([[0/10.0]])
)

# Set surfaces
s1 = mcdc.surface("plane-x", x=0.0, bc="reflective")
s2 = mcdc.surface("plane-x", x=1.0, bc="reflective")
#s3 = mcdc.surface("plane-x", x=2.0, bc="reflective")

# Set cells
mcdc.cell([+s1, -s2], m1)
#mcdc.cell([+s2, -s3], m2)

# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

Nx = 20
Nmu = 2

# Tally: cell-average and cell-edge angular fluxes and currents
mcdc.tally(
    scores=["flux", "flux-x"],
    x=np.linspace(0.0, 1.0, Nx + 1),
    mu=np.linspace(-1.0, 1.0, Nmu + 1)
)

# =============================================================================
# Residual Parameters
# =============================================================================

hi = 1.0 / Nx
hj = 2.0 / Nmu
estimate = np.zeros([Nx, Nmu])

estimate = np.ones([Nx, Nmu]) * 2
#with h5py.File("rmc1e6noestimate.h5", "r") as f:
    #estimate = f["tally/flux/mean"][:]

#with h5py.File("output.h5", "r") as f:
    #estimate = f["tally/flux/mean"][:]

#fixed_source = np.zeros([Nx, Nmu]) * Nx * Nmu
#fixed_source[0,0] = Nx*Nmu
#fixed_source[0,1] = Nx*Nmu
fixed_source = np.ones([Nx, Nmu])

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