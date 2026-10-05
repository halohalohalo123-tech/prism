import os

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

LIBRARY_DIR = "data/usgs_library"

# grid spacing in micrometres (1 nm, the spacing of the USGS files)
BAND_STEP = 0.001


def load_usgs_spectrum(file_path):
    """
    Reads one USGS-style csv and returns (wavelength, reflectance)
    containing ONLY the valid measurements, sorted by wavelength.
    """

    df = pd.read_csv(file_path)

    # the csv headers have trailing spaces ("Wavelength ")
    df.columns = [c.strip() for c in df.columns]

    wl = df["Wavelength"].to_numpy(dtype=float)

    refl = df["Reflectance"].to_numpy(dtype=float)

    # The wavelength column is rounded to 3 significant digits, so above
    # 1 um many rows share the same value (1.50, 1.50, 1.50 ...).
    # The data is evenly spaced, so rebuild the true wavelengths.
    is_sorted = np.all(np.diff(wl) >= 0)

    if is_sorted and len(np.unique(wl)) < 0.9 * len(wl):

        wl = np.linspace(wl.min(), wl.max(), len(wl))

    # USGS marks missing data with -1.23e34
    valid = (
        np.isfinite(refl)
        & np.isfinite(wl)
        & (refl > -1e30)
    )

    wl = wl[valid]

    refl = refl[valid]

    order = np.argsort(wl, kind="stable")

    return wl[order], refl[order]


def common_grid(spectra):
    """
    Wavelength grid covered by EVERY spectrum.
    (Some library minerals only have data in part of the range,
    so comparing them on a longer grid would be wrong.)
    """

    lo = max(wl.min() for wl, _ in spectra)

    hi = min(wl.max() for wl, _ in spectra)

    if hi <= lo:

        raise ValueError(
            "The library spectra do not overlap in wavelength."
        )

    n = int(round((hi - lo) / BAND_STEP)) + 1

    return np.linspace(lo, hi, n)


def resample_spectrum(wavelength, reflectance, grid):
    """
    Interpolates a spectrum onto the shared grid.
    Never extrapolates: if the spectrum does not cover the grid,
    it is an error (extrapolated numbers would be invented data).
    """

    tol = 1e-6

    if (wavelength.min() > grid.min() + tol
            or wavelength.max() < grid.max() - tol):

        raise ValueError(
            "This spectrum covers %.3f-%.3f um but the analysis needs "
            "%.3f-%.3f um." % (
                wavelength.min(), wavelength.max(),
                grid.min(), grid.max()
            )
        )

    f = interp1d(wavelength, reflectance, kind="linear")

    # (grid may exceed the data by a rounding error of ~1e-16)
    return f(np.clip(grid, wavelength.min(), wavelength.max()))


def load_usgs_library():
    """
    Returns (library, mineral_names, grid)
        library : (n_minerals, n_bands) reflectance on the shared grid
        grid    : the wavelengths (um) of those bands
    """

    files = sorted(
        f for f in os.listdir(LIBRARY_DIR)
        if f.endswith(".csv")
    )

    spectra = [
        load_usgs_spectrum(os.path.join(LIBRARY_DIR, f))
        for f in files
    ]

    grid = common_grid(spectra)

    library = np.array([
        resample_spectrum(wl, refl, grid)
        for wl, refl in spectra
    ])

    mineral_names = [f[:-4] for f in files]

    return library, mineral_names, grid