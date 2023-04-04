import numpy as np
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
m = mcdc.material(
    capture=np.array([100.0/100.0]),
    scatter=np.array([[0.0/100.0]])
)

# Set surfaces
s1 = mcdc.surface("plane-x", x=0, bc="reflective")
s2 = mcdc.surface("plane-x", x=1.0, bc="reflective")

# Set cells
mcdc.cell([+s1, -s2], m)

# =============================================================================
# Set source
# =============================================================================
# Isotropic pulse at x=t=0

mcdc.source(x=[0.0, 1.0], isotropic=True)

# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

# Tally: cell-average and cell-edge angular fluxes and currents

Nx = 20
Nmu = 2

mcdc.tally(
    scores=["flux", "flux-x"],
    x=np.linspace(0.0, 1.0, Nx + 1),
    mu=np.linspace(-1.0, 1.0, Nmu + 1)
)

# Setting
mcdc.setting(N_particle=1e6)

# Run
mcdc.run()
