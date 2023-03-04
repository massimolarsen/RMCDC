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
    capture=np.array([1.0 / 2.0]),
    scatter=np.array([[1.0 / 2.0]])
)

# Set surfaces
s1 = mcdc.surface("plane-x", x=0, bc="reflective")
s2 = mcdc.surface("plane-x", x=6.0, bc="reflective")

# Set cells
mcdc.cell([+s1, -s2], m)

# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

# Tally: cell-average and cell-edge angular fluxes and currents
mcdc.tally(
    scores=["flux", "flux-x"],
    x=np.linspace(0.0, 6.0, 61),
    mu=np.linspace(-1.0, 1.0, 32 + 1)
)

# =============================================================================
# Residual Parameters
# =============================================================================

hi = 0.1
hj = 2.0 / 32.0
estimate = np.zeros([60, 32])
fixed_source = np.ones([60, 32])
interior_integral = np.zeros_like(estimate)
face_integral = np.zeros_like(estimate)
interior_residual = np.zeros_like(estimate)
face_residual = np.zeros_like(estimate)
residual_source = np.zeros_like(estimate)

mcdc.residual(
    hi=hi,
    hj=hj,
    estimate=estimate,
    fixed_source=fixed_source,
    interior_integral=interior_integral,
    face_integral=face_integral,
    interior_residual=interior_residual,
    face_residual=face_residual,
    residual_source=residual_source
)

# Setting
mcdc.setting(N_particle=1e5)

# Run
mcdc.run()
