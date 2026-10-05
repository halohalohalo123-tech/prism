import numpy as np


def reconstruction_loss(
        original,
        reconstructed):
    """
    Relative reconstruction error: 0 = perfect, ~1 = the unmixing
    explains nothing. Scale-free, so it does not depend on the
    units of the spectrum.
    """

    energy = np.mean(original ** 2)

    error = np.mean(
        (original - reconstructed) ** 2
    )

    return error / max(energy, 1e-12)


def uncertainty(probabilities):

    return 1.0 - np.max(probabilities)


def anomaly_score(
        reconstruction,
        uncertainty_val):
    """Both inputs are 0-1, so the score is 0-1."""

    return (
        0.6 * min(reconstruction, 1.0) +
        0.4 * uncertainty_val
    )