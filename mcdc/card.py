import numpy as np

from mcdc.constant import INF, GR_ALL, PCT_NONE, PI


class InputCard:
    def __init__(self):
        self.reset()

    def reset(self):
        self.nuclides = []
        self.materials = []
        self.surfaces = []
        self.cells = []
        self.universes = [{}]
        self.lattices = []
        self.sources = []

        # Root universe
        self.universes[0] = {
            "tag": "Universe",
            "ID": 0,
            "N_cell": 0,
            "cell_IDs": np.array(0),
        }

        self.tally = {
            "tag": "Tally",
            "tracklength": False,
            "flux": False,
            "density": False,
            "fission": False,
            "total": False,
            "current": False,
            "eddington": False,
            "crossing": False,
            "crossing_x": False,
            "flux_x": False,
            "density_x": False,
            "fission_x": False,
            "total_x": False,
            "current_x": False,
            "eddington_x": False,
            "crossing_y": False,
            "flux_y": False,
            "density_y": False,
            "fission_y": False,
            "total_y": False,
            "current_y": False,
            "eddington_y": False,
            "crossing_z": False,
            "flux_z": False,
            "density_z": False,
            "fission_z": False,
            "total_z": False,
            "current_z": False,
            "eddington_z": False,
            "crossing_t": False,
            "flux_t": False,
            "density_t": False,
            "fission_t": False,
            "total_t": False,
            "current_t": False,
            "eddington_t": False,
            "mesh": {
                "x": np.array([-INF, INF]),
                "y": np.array([-INF, INF]),
                "z": np.array([-INF, INF]),
                "t": np.array([-INF, INF]),
                "mu": np.array([-1.0, 1.0]),
                "azi": np.array([-PI, PI]),
            },
        }

        self.setting = {
            "tag": "Setting",
            "N_particle": 0,
            "N_inactive": 0,
            "N_active": 0,
            "N_cycle": 0,
            "mode_eigenvalue": False,
            "time_boundary": INF,
            "rng_seed": 1,
            "rng_stride": 152917,
            "rng_g": 2806196910506780709,
            "rng_c": 1,
            "rng_mod": 2**63,
            "bank_active_buff": 100,
            "bank_census_buff": 1.0,
            "N_cycle_buff": 0,
            "k_init": 1.0,
            "output": "output",
            "progress_bar": True,
            "gyration_radius": False,
            "gyration_radius_type": GR_ALL,
            "filed_source": False,
            "source_file": "",
        }

        self.technique = {
            "tag": "Technique",
            "weighted_emission": True,
            "implicit_capture": False,
            "branchless_collision": False,
            "population_control": False,
            "pct": PCT_NONE,
            "weight_window": False,
            "ww": np.ones([1, 1, 1, 1]),
            "ww_mesh": {
                "x": np.array([-INF, INF]),
                "y": np.array([-INF, INF]),
                "z": np.array([-INF, INF]),
                "t": np.array([-INF, INF]),
                "mu": np.array([-1.0, 1.0]),
                "azi": np.array([-PI, PI]),
            },
            "time_census": False,
            "census_time": np.array([INF]),
            "IC_generator": False,
            "IC_N_neutron": 0,
            "IC_N_precursor": 0,
            "weight_roulette": False,
            "wr_threshold": 0.0,
            "wr_target": 1.0,
            "iQMC": False,
            "iqmc_generator": "sobol",
            "iqmc_tol": 1e-6,
            "iqmc_res": 1.0,
            "iqmc_itt": 0,
            "iqmc_maxitt": 5,
            "iqmc_N_dim": 6,
            "iqmc_seed": 12345,
            "iqmc_scramble": False,
            "iqmc_fixed_source": np.ones([1, 1, 1, 1]),
            "iqmc_material_idx": np.ones([1, 1, 1, 1]),
            "iqmc_flux": np.ones([1, 1, 1, 1]),
            "iqmc_mesh": {
                "x": np.array([-INF, INF]),
                "y": np.array([-INF, INF]),
                "z": np.array([-INF, INF]),
                "t": np.array([-INF, INF]),
                "mu": np.array([-1.0, 1.0]),
                "azi": np.array([-PI, PI]),
            },
            "sensitivity": 0,
            "sensitivity_N": 0,
        }


class SurfaceHandle:
    def __init__(self, card):
        self.card = card

    def __pos__(self):
        return [self.card, True]

    def __neg__(self):
        return [self.card, False]
