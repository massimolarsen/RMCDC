import numpy as np

from mcdc.constant import INF

class InputCard:
    def __init__(self):
        self.reset()

    def reset(self):
        self.materials = []
        self.surfaces  = []
        self.cells     = []
        self.sources   = []
        self.tally     = {'tag'         : 'Tally',
                          'tracklength' : False,
                          'flux'        : False,
                          'current'     : False,
                          'eddington'   : False,
                          'crossing'    : False,
                          'crossing_x'  : False,
                          'crossing_t'  : False,
                          'flux_x'      : False,
                          'flux_t'      : False,
                          'current_x'   : False,
                          'current_t'   : False,
                          'eddington_x' : False,
                          'eddington_t' : False,
                          'mesh'        : {'x' : np.array([-INF, INF]),
                                           'y' : np.array([-INF, INF]),
                                           'z' : np.array([-INF, INF]),
                                           't' : np.array([-INF, INF])}}
        self.setting   = {'tag'                : 'Setting',
                          'N_hist'             : 0,
                          'N_iter'             : 1,
                          'mode_eigenvalue'    : False,
                          'mode_alpha'         : False,
                          'time_boundary'      : INF,
                          'rng_seed'           : 1,
                          'rng_stride'         : 152917,
                          'k_init'             : 1.0,
                          'alpha_init'         : 0.0,
                          'output'             : 'output',
                          'progress_bar'       : True}
        self.technique = {'tag'                : 'Technique', 
                          'weighted_emission'  : True,
                          'implicit_capture'   : False,
                          'population_control' : False,
                          'weight_window'      : False,
                          'ww'                 : np.ones([1,1,1,1]), 
                          'ww_mesh'            : {'x' : np.array([-INF, INF]),
                                                  'y' : np.array([-INF, INF]),
                                                  'z' : np.array([-INF, INF]),
                                                  't' : np.array([-INF, INF])}}

class SurfaceHandle:
    def __init__(self, card):
        self.card = card
    def __pos__(self):
        return [self.card, True]
    def __neg__(self):
        return [self.card, False]