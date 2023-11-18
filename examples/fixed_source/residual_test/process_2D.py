import matplotlib.pyplot as plt
import h5py
import numpy as np


phi = np.sum(np.array([[[4.99956336, 4.99990169, 5.00002407, 5.00000099],
  [1.66659425, 1.66663293, 1.66664876, 1.66666114]],

 [[2.49981236, 2.49972157, 2.50002624, 2.50003183],
  [1.2499384,  1.24997771, 1.24999352, 1.25000439]]]),2)


error = np.array([[16.94867936721402, 3.898718244924563, 1.339997909494284, 0.5625453820150893, 0.2288316210366509, 0.09595226032033595, 0.04801921952994677, 0.024716101552304304, 0.013477407058749467, 0.007340075532596418, 0.003622306165947585, 0.0017540821394725398, 0.0008250938228230172, 0.00040545803678580686, 0.00017481151102850432, 8.189039518508144e-05, 3.406489230815651e-05, 1.4930374483265525e-05, 6.098176951333921e-06, 2.5699846502621037e-06, 1.203436852801427e-06, 4.870212135288468e-07, 2.0306739452865645e-07, 8.632159547311283e-08, 3.7272923205234334e-08, 1.4023472826062285e-08, 5.999549005571622e-09, 2.4891468751618566e-09, 1.0803037579057382e-09, 4.445222224402058e-10, 1.9317364852911076e-10, 7.749224075015407e-11, 3.154659827026393e-11, 1.249098249919762e-11, 4.9238461566806245e-12, 2.062150565753569e-12, 8.415429282971982e-13, 3.426932516123781e-13, 1.278167890955926e-13, 5.2452990932664756e-14, 2.0220786716511845e-14, 8.083779242109936e-15, 3.300121544232944e-15, 1.094245316235302e-15, 5.517689712290712e-16]])


# Plot result
X, Y = np.meshgrid([0,6], [0,6])
print(X)