import numpy as np
import itertools

Qs = [
    np.array([0.5482, 0.2114, -0.5895, 1.2889, 0.2974, 0.2614, 0.2543]),
    np.array([1.3778, 0.9488, -1.2763, 0.9267, 1.5707, 0.0, 0.0]),
    np.array([2.1644, 0.9734, -1.311, 0.5538, 1.5411, 0.0034, -0.0019]),
    np.array([0.4744, 1.1553, -1.0282, 0.593, 1.5411, 0.0034, -0.0019]),
]

S1, S2, S3, S4 = np.array(list(itertools.combinations(Qs, 3)))
S_all = [S1, S2, S3, S4]

V1 = Qs[3]
V2 = Qs[2]
V3 = Qs[1]
V4 = Qs[0]

V_all = [V1, V2, V3, V4]