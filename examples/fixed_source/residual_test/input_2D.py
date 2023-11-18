import numpy as np
import h5py
import sys
sys.path.append('C:/users/larse/source/repos/RMCDC')
import mcdc

# =============================================================================
# Set model
# =============================================================================

X = 8.0
Y = 8.0

# Set materials
m1 = mcdc.material(
    capture=np.array([1.0]),
    scatter=([[0.0]])
)

m2 = mcdc.material(
    capture=np.array([4.0]),
    scatter=([[0.0]])
)


# Set surfaces
sx1 = mcdc.surface("plane-x", x=0.0, bc="vacuum")
sx2 = mcdc.surface("plane-x", x=4.0)
sx3 = mcdc.surface("plane-x", x=X, bc="vacuum")
sy1 = mcdc.surface("plane-y", y=0.0, bc="vacuum")
sy2 = mcdc.surface("plane-y", y=4.0)
sy3 = mcdc.surface("plane-y", y=Y, bc="vacuum")


# Set cells

# bottom left
mcdc.cell([+sx1, -sx2, +sy1, -sy2], m2)
# bottom right
mcdc.cell([+sx2, -sx3, +sy1, -sy2], m1)
# top left
mcdc.cell([+sx1, -sx2, +sy2, -sy3], m1)
# top right
mcdc.cell([+sx2, -sx3, +sy2, -sy3], m1)

# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

Nx = 2
Ny = 2
N_azi = 4

# Tally: cell-average and cell-edge angular fluxes and currents
mcdc.tally(
    scores=["flux"],
    x=np.linspace(0.0, X, Nx + 1),
    y=np.linspace(0.0, Y, Ny + 1),
    azi=np.linspace(-np.pi, np.pi, N_azi + 1)
)

# =============================================================================
# Residual Parameters
# =============================================================================

hi = X / Nx
hj = Y / Ny
hk = 2*np.pi / N_azi

estimate = np.ones((Nx, Ny, N_azi)) * 1

fixed_source = np.ones((Nx, Ny, N_azi)) * 5

interior_integral = np.zeros_like(fixed_source)
face_integral = np.zeros_like(fixed_source)
interior_residual = np.zeros_like(fixed_source)
face_residual = np.zeros_like(fixed_source)
residual_norm = np.zeros_like(fixed_source)

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
    residual_norm=residual_norm,
    exponential_convergence=exponential_convergence
)

# Setting
mcdc.setting(N_particle=1e4)

# Run
mcdc.run()