import numpy as np
import h5py

import mcdc


def test():
    # =========================================================================
    # Set model and run
    # =========================================================================

    with np.load("CASMO-70.npz") as data:
        SigmaC = data["SigmaC"] * 1.28  # /cm
        SigmaS = data["SigmaS"]
        SigmaF = data["SigmaF"]
        nu_p = data["nu_p"]
        nu_d = data["nu_d"]
        chi_p = data["chi_p"]
        chi_d = data["chi_d"]
        G = data["G"]
        speed = data["v"]
        lamd = data["lamd"]

    m = mcdc.material(
        capture=SigmaC,
        scatter=SigmaS,
        fission=SigmaF,
        nu_p=nu_p,
        chi_p=chi_p,
        nu_d=nu_d,
        chi_d=chi_d,
        decay=lamd,
        speed=speed,
    )

    s1 = mcdc.surface("plane-x", x=-1e10, bc="reflective")
    s2 = mcdc.surface("plane-x", x=1e10, bc="reflective")

    c = mcdc.cell([+s1, -s2], m)

    energy = np.zeros(G)
    energy[-1] = 1.0
    source = mcdc.source(energy=energy)

    scores = ["flux-t"]
    mcdc.tally(scores=scores, t=np.insert(np.logspace(-8, 1, 100), 0, 0.0))

    mcdc.setting(N_particle=1e1, progress_bar=False)

    mcdc.run()

    # =========================================================================
    # Check output
    # =========================================================================

    output = h5py.File("output.h5", "r")
    answer = h5py.File("answer.h5", "r")
    for score in scores:
        name = "tally/" + score + "/mean"
        a = output[name][:]
        b = answer[name][:]
        assert np.isclose(a, b).all()

        name = "tally/" + score + "/sdev"
        a = output[name][:]
        b = answer[name][:]
        assert np.isclose(a, b).all()

    output.close()
    answer.close()
