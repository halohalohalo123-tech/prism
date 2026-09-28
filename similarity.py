import numpy as np


def SAM(a, b):

    dot = np.dot(a, b)

    denom = (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )

    denom = max(denom, 1e-10)

    value = np.clip(
        dot / denom,
        -1,
        1
    )

    return np.arccos(value)