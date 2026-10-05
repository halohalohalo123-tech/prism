"""
Creates test samples with a KNOWN composition, so the unmixing can be
checked against the right answer:   python make_test_samples.py

The mixtures are built with the Kubelka-Munk rule used by the pipeline
(F(R) of a mixture = weighted sum of the F(R) of its minerals).
IMPORTANT: they are made from the same library spectra, so they test
the unmixing, NOT the ability to recognise a brand-new natural sample.
For that, add independent USGS spectra to data/samples/.
"""

import numpy as np
import pandas as pd

from loader import load_usgs_library
from preprocessing import kubelka_munk

NOISE = 0.003

TEST_SAMPLES = {
    "mix_quartz60_kaolinite40": {"Quartz": 0.6, "Kaolinite": 0.4},
    "mix_basalt20_hematite45_jarosite35": {
        "Basalt": 0.2, "Hematite": 0.45, "Jarosite": 0.35
    },
    "mix_anorthite60_pyroxene40": {"Anorthite": 0.6, "Pyroxene": 0.4},
}


def inverse_kubelka_munk(f):

    return 1 + f - np.sqrt(f ** 2 + 2 * f)


def mix_spectrum(library, names, recipe):

    f = sum(
        w * kubelka_munk(library[names.index(n)])
        for n, w in recipe.items()
    )

    return inverse_kubelka_munk(f)


if __name__ == "__main__":

    library, names, grid = load_usgs_library()

    rng = np.random.default_rng(2026)

    for file_name, recipe in TEST_SAMPLES.items():

        refl = mix_spectrum(library, names, recipe)

        refl = refl + rng.normal(0, NOISE, refl.shape)

        df = pd.DataFrame({
            "Reflectance ": refl,
            "Wavelength ": grid
        })

        path = "data/samples/%s.csv" % file_name

        df.to_csv(path, index=False, float_format="%.6e")

        print("written", path, recipe)