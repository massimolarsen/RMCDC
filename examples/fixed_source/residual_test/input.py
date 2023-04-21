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


# Set surfaces
sx1 = mcdc.surface("plane-x", x=0.0, bc="vacuum")
sx2 = mcdc.surface("plane-x", x=1.0, bc="vacuum")
sy1 = mcdc.surface("plane-y", y=0.0, bc="vacuum")
sy2 = mcdc.surface("plane-y", y=1.0, bc="vacuum")


# Set cells
mcdc.cell([+sx1, -sx2, +sy1, -sy2], m1)

# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

Nx = 2
Ny = 2
N_azi = 4

# Tally: cell-average and cell-edge angular fluxes and currents
mcdc.tally(
    scores=["flux"],
    x=np.linspace(0.0, 1.0, Nx + 1),
    y=np.linspace(0.0, 1.0, Ny + 1),
    azi=np.linspace(np.pi/4, 9*np.pi/4, N_azi + 1)
)

# =============================================================================
# Residual Parameters
# =============================================================================

hi = 1.0 / Nx
hj = 1.0 / Ny
hk = 2*np.pi / N_azi

estimate = np.ones((Nx, Ny, N_azi)) * 1

fixed_source = np.ones((Nx, Ny, N_azi)) * 5

interior_integral = np.zeros_like(fixed_source)
face_integral = np.zeros_like(fixed_source)
interior_residual = np.zeros_like(fixed_source)
face_residual = np.zeros_like(fixed_source)
residual_source = np.zeros_like(fixed_source)

exponential_convergence = True

mcdc.residual(
    hi=hi,
    hj=hj,
    hk=hk,
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