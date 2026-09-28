import numpy as np
from scipy.optimize import nnls


def FCLS(sample, library):

    coeffs = []

    for mineral in library:

        c, _ = nnls(
            mineral.reshape(-1, 1),
            sample
        )

        coeffs.append(c[0])

    coeffs = np.array(coeffs)

    coeffs = coeffs / coeffs.sum()

    return coeffs