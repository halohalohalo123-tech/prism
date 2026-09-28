import os
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

TARGET_BANDS = 2152


def load_usgs_spectrum(file_path):

    df = pd.read_csv(file_path)

    df = df.replace(-1.23e34, np.nan)

    df = df.dropna()

    df = df.sort_values("Wavelength ")

    wl = df["Wavelength "].values

    refl = df["Reflectance "].values

    return wl, refl


def resample_spectrum(wavelength, reflectance):

    new_wl = np.linspace(
        wavelength.min(),
        wavelength.max(),
        TARGET_BANDS
    )

    f = interp1d(
        wavelength,
        reflectance,
        kind="linear",
        fill_value="extrapolate"
    )

    new_reflectance = f(new_wl)

    return new_wl, new_reflectance


def load_usgs_library():

    library = []

    mineral_names = []

    folder = "data/usgs_library"

    for file in os.listdir(folder):

        if file.endswith(".csv"):

            path = os.path.join(folder, file)

            wl, refl = load_usgs_spectrum(path)

            wl, refl = resample_spectrum(
                wl,
                refl
            )

            library.append(refl)

            mineral_names.append(
                file.replace(".csv", "")
            )

    return np.array(library), mineral_names