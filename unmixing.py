import numpy as np
from scipy.optimize import nnls


def FCLS(sample, library, delta=1e3):
    """
    Fully Constrained Least Squares unmixing.

    Solves ALL minerals together:
        sample  ~  sum_i( a_i * library_i )
    with  a_i >= 0  (non-negativity)  and  sum(a_i) = 1  (sum-to-one).

    The sum-to-one rule is enforced by adding one extra row of
    (delta * 1) to the problem, a standard FCLS trick.
    """

    # shape: (bands, minerals)
    A = library.T

    A_aug = np.vstack([
        A,
        delta * np.ones((1, A.shape[1]))
    ])

    b_aug = np.append(sample, delta)

    abundances, _ = nnls(
        A_aug,
        b_aug,
        maxiter=10000
    )

    # remove any tiny numerical drift from exactly 1
    total = abundances.sum()

    if total > 0:
        abundances = abundances / total

    return abundances