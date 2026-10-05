import numpy as np

from scipy.signal import savgol_filter

# ---------------------------------------------------------------
# Settings (chosen from the noise tests in evaluate.py)
# ---------------------------------------------------------------

SMOOTH_WINDOW = 11      # Savitzky-Golay window (bands = nm)
SMOOTH_POLY = 3

# Kubelka-Munk is F(R) = (1-R)^2 / (2R). It explodes when R -> 0:
# at R = 0.001 a noise of 0.005 changes F by ~ 2500. Reflectance is
# therefore clipped at 0.02 (largest F = 24) to keep it stable.
KM_MIN_REFLECTANCE = 0.02
KM_MAX_REFLECTANCE = 0.999


def smooth_signal(signal):

    return savgol_filter(
        signal,
        window_length=SMOOTH_WINDOW,
        polyorder=SMOOTH_POLY
    )


def kubelka_munk(reflectance):
    """
    Kubelka-Munk remission function F(R) = (1 - R)^2 / (2R).
    Must be applied to REAL reflectance (not to a rescaled spectrum),
    because F(R) is what mixes linearly for powdered mixtures.
    """

    reflectance = np.clip(
        reflectance,
        KM_MIN_REFLECTANCE,
        KM_MAX_REFLECTANCE
    )

    return ((1 - reflectance) ** 2) / (
        2 * reflectance
    )


def preprocess(reflectance):
    """
    The ONE preprocessing pipeline.
    Used for: training, the mineral library, and new samples.

        smoothing  ->  Kubelka-Munk

    No continuum removal / min-max normalization here: tests showed
    they multiply the noise by 13-40x and remove the brightness and
    slope information that separates featureless minerals (e.g. quartz).
    """

    reflectance = smooth_signal(reflectance)

    reflectance = kubelka_munk(reflectance)

    return reflectance


def continuum_removal(spectrum):
    """
    True continuum removal (upper convex hull).
    NOT part of the main pipeline; kept for absorption-band analysis
    (band depth / position), where it is meant to be used.
    """

    x = np.arange(len(spectrum))

    hull = []

    for i in range(len(spectrum)):

        while len(hull) >= 2:

            x1, y1 = hull[-2]
            x2, y2 = hull[-1]

            cross = (
                (x2 - x1) * (spectrum[i] - y1)
                - (y2 - y1) * (x[i] - x1)
            )

            if cross >= 0:
                hull.pop()
            else:
                break

        hull.append((x[i], spectrum[i]))

    hx, hy = zip(*hull)

    continuum = np.interp(x, hx, hy)

    return spectrum / np.maximum(continuum, 1e-10)