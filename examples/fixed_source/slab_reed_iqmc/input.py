import numpy as np

import mcdc

# =============================================================================
# Set model
# =============================================================================
# Three slab layers with different materials
# Based on William H. Reed, NSE (1971), 46:2, 309-314, DOI: 10.13182/NSE46-309

# Set materials
m1 = mcdc.material(capture=np.array([50.0]))
m2 = mcdc.material(capture=np.array([5.0]))
m3 = mcdc.material(capture=np.array([0.0]))  # Vacuum
m4 = mcdc.material(capture=np.array([0.1]), scatter=np.array([[0.9]]))

# Set surfaces
s1 = mcdc.surface("plane-x", x=-8.0, bc="vacuum")
s2 = mcdc.surface("plane-x", x=-5.0)
s3 = mcdc.surface("plane-x", x=-3.0)
s4 = mcdc.surface("plane-x", x=-2.0)
s5 = mcdc.surface("plane-x", x=2.0)
s6 = mcdc.surface("plane-x", x=3.0)
s7 = mcdc.surface("plane-x", x=5.0)
s8 = mcdc.surface("plane-x", x=8.0, bc="vacuum")

# Set cells
mcdc.cell([+s1, -s2], m4)
mcdc.cell([+s2, -s3], m3)
mcdc.cell([+s3, -s4], m2)
mcdc.cell([+s4, -s5], m1)
mcdc.cell([+s5, -s6], m2)
mcdc.cell([+s6, -s7], m3)
mcdc.cell([+s7, -s8], m4)


# =============================================================================
# iQMC Parameters
# =============================================================================
N = 1e2
Nx = 32
maxit = 5
tol = 1e-3
x = np.linspace(-8, 8, num=Nx + 1)
generator = "halton"

fixed_source = np.zeros(Nx)
fixed_source[int(0.375 * Nx) : int(0.625 * Nx)] = 50.0
fixed_source[int(0.125 * Nx) : int(0.1875 * Nx)] = 1.0
fixed_source[int(0.8125 * Nx) : int(0.875 * Nx)] = 1.0

material_idx = np.zeros(Nx, dtype=int)
material_idx[: int(0.1875 * Nx)] = 3
material_idx[int(0.1875 * Nx) : int(0.3125 * Nx)] = 2
material_idx[int(0.3125 * Nx) : int(0.375 * Nx)] = 1
material_idx[int(0.625 * Nx) : int(0.6875 * Nx)] = 1
material_idx[int(0.6875 * Nx) : int(0.8125 * Nx)] = 2
material_idx[int(0.8125 * Nx) :] = 3

phi0 = np.ones((Nx))

mcdc.iQMC(
    x=x,
    fixed_source=fixed_source,
    phi0=phi0,
    material_idx=material_idx,
    maxitt=maxit,
    tol=tol,
    generator=generator,
)

# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

# Setting
mcdc.setting(N_particle=N, progress_bar=True)

# Run
mcdc.run()
