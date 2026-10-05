"""
Measures how well the system works:   python evaluate.py
(run  python train_model.py  first)
"""

import numpy as np

from loader import load_usgs_library
from preprocessing import preprocess, kubelka_munk
from unmixing import FCLS
from classifier import MineralClassifier
from pipeline import load_context, analyze
from make_test_samples import (
    TEST_SAMPLES,
    inverse_kubelka_munk
)

NOISE_LEVELS = (0, 0.005, 0.02, 0.05)

library, names, grid = load_usgs_library()

clean_library = np.array([preprocess(s) for s in library])


def random_mixtures(n=25, seed=1):

    rng = np.random.default_rng(seed)

    out = []

    for _ in range(n):

        k = rng.integers(2, 4)

        idx = rng.choice(len(names), k, replace=False)

        t = np.zeros(len(names))

        t[idx] = rng.dirichlet(np.ones(k))

        out.append(t)

    return out


def make_mix(t, rule):

    if rule == "reflectance":

        return t @ library

    f = t @ np.array([kubelka_munk(s) for s in library])

    return inverse_kubelka_munk(f)


print("=" * 64)
print("1) UNMIXING on 25 random mixtures of 2-3 minerals")
print("   error = RMSE between true and estimated abundances (0 = perfect)")
print("=" * 64)

for rule, text in [
        ("km", "mixed with the Kubelka-Munk rule (powders; the pipeline's model)"),
        ("reflectance", "mixed linearly in reflectance (side-by-side patches)")]:

    print("\n  mixtures", text)

    for nz in NOISE_LEVELS:

        errors = []

        for t in random_mixtures():

            clean = make_mix(t, rule)

            for seed in range(3):

                rng = np.random.default_rng(100 + seed)

                noisy = clean + (
                    rng.normal(0, nz, clean.shape) if nz else 0
                )

                est = FCLS(preprocess(noisy), clean_library)

                errors.append(np.sqrt(np.mean((est - t) ** 2)))

        print("    noise %.3f -> error %.3f" % (nz, np.mean(errors)))

print()
print("=" * 64)
print("2) CLASSIFIER on library spectra with NEW random noise")
print("=" * 64)

clf = MineralClassifier("models/random_forest.pkl")

rng = np.random.default_rng(12345)

for nz in NOISE_LEVELS:

    ok, conf, total = 0, [], 0

    for spectrum, name in zip(library, names):

        for _ in range(30):

            x = preprocess(spectrum + rng.normal(0, nz, spectrum.shape))

            label, c, _ = clf.predict(x)

            ok += (label == name)

            conf.append(c)

            total += 1

    print("  noise %.3f -> accuracy %.0f%%, mean confidence %.2f" % (
        nz, 100 * ok / total, np.mean(conf)
    ))

print()
print("=" * 64)
print("3) TEST SAMPLES with known composition (data/samples/)")
print("=" * 64)

for file_name, recipe in TEST_SAMPLES.items():

    ctx = load_context("data/samples/%s.csv" % file_name)

    r = analyze(ctx)

    print("\n  %s" % file_name)

    print("    true     :", {k: "%d%%" % round(v * 100) for k, v in recipe.items()})

    est = {
        n: "%d%%" % round(a * 100)
        for n, a in zip(r["mineral_names"], r["abundances"])
        if a >= 0.02
    }

    print("    estimated:", est)

    print("    planet: %s | classifier says: %s (confidence %.2f)" % (
        r["planet"], r["label"], r["confidence"]
    ))