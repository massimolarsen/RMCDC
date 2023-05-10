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
    capture=np.array([1.1]),
    scatter=np.array([[0.9]])
)

m2 = mcdc.material(
    capture=np.array([0])
)

m3 = mcdc.material(
    capture=np.array([1.0])
)

m4 = mcdc.material(
    capture=np.array([2.0])
)

# Set surfaces
s1 = mcdc.surface("plane-z", z=0, bc="vacuum")
s2 = mcdc.surface("plane-z", z=4.0)
s3 = mcdc.surface("plane-z", z=6.0)
s4 = mcdc.surface("plane-z", z=8.0, bc="vacuum")

# Set cells
mcdc.cell([+s1, -s2], m3)
mcdc.cell([+s2, -s3], m3)
mcdc.cell([+s3, -s4], m3)


# =============================================================================
# Set tally, setting, and run mcdc
# =============================================================================

Nz = 10
Nmu = 2
Nt = 10

# Tally: cell-average and cell-edge angular fluxes and currents
mcdc.tally(
    scores=["flux", "flux-t"],
    z=np.linspace(0.0, 8.0, Nz + 1),
    mu=np.linspace(-1.0, 1.0, Nmu + 1),
    t=np.linspace(0.0, 10.0, Nt + 1)
)

# =============================================================================
# Residual Parameters
# =============================================================================

hi = 8.0 / Nz
hj = 2.0 / Nmu
ht = 10.0 / Nt

estimate = np.ones([Nz, Nmu, Nt]) * 0

#estimate = np.array([[6,0],[6,0],[6,0]])


#with h5py.File("rmc1e6noestimate.h5", "r") as f:
    #estimate = f["tally/flux/mean"][:]

#with h5py.File("output.h5", "r") as f:
    #estimate = f["tally/flux/mean"][:]

#fixed_source = np.zeros([Nx, Nmu]) * Nx * Nmu
#fixed_source[0,0] = Nx*Nmu
#fixed_source[0,1] = Nx*Nmu

fixed_source = np.ones([Nz, Nmu, Nt]) * 0

#for i in range(10):
    #fixed_source[i+10,:] = 1
    #fixed_source[i+30,:] = 50

fixed_source = np.ones([Nz, Nmu, Nt]) * 5

interior_integral = np.zeros_like(fixed_source)
face_integral = np.zeros_like(fixed_source)
interior_residual = np.zeros_like(fixed_source)
face_residual = np.zeros_like(fixed_source)
residual_norm = np.zeros_like(fixed_source)

exponential_convergence = True

mcdc.residual(
    hi=hi,
    hj=hj,
    ht=ht,
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