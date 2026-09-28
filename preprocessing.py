import numpy as np

from scipy.signal import savgol_filter
from sklearn.preprocessing import MinMaxScaler


def smooth_signal(signal):

    return savgol_filter(
        signal,
        window_length=11,
        polyorder=3
    )


def continuum_removal(spectrum):

    hull = np.maximum.accumulate(spectrum)

    hull[hull == 0] = 1e-10

    return spectrum / hull


def normalize_spectrum(spectrum):

    scaler = MinMaxScaler()

    return scaler.fit_transform(
        spectrum.reshape(-1, 1)
    ).flatten()


def kubelka_munk(reflectance):

    reflectance = np.clip(
        reflectance,
        1e-6,
        0.999999
    )

    return ((1 - reflectance) ** 2) / (
        2 * reflectance
    )