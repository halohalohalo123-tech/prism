import numpy as np


def reconstruction_loss(
        original,
        reconstructed):

    return np.mean(
        (original - reconstructed) ** 2
    )


def uncertainty(probabilities):

    return 1.0 - np.max(probabilities)


def anomaly_score(
        reconstruction,
        uncertainty_val):

    return (
        0.6 * reconstruction +
        0.4 * uncertainty_val
    )