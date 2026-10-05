import numpy as np

from loader import (
    load_usgs_library,
    load_usgs_spectrum,
    resample_spectrum
)
from preprocessing import preprocess
from unmixing import FCLS
from similarity import SAM
from classifier import MineralClassifier
from anomaly import (
    reconstruction_loss,
    uncertainty,
    anomaly_score
)
from planetary import detect_planetary_origin
from expert_system import check_geological_consistency


def load_context(
        sample_path="data/samples/sample.csv",
        model_path="models/random_forest.pkl"):
    """
    Loads everything that does NOT change between analyses:
    the preprocessed library, the raw sample, and the model.
    Done once, then reused (so the dashboard slider is fast).
    """

    library, mineral_names, grid = load_usgs_library()

    library = np.array([
        preprocess(spectrum)
        for spectrum in library
    ])

    wl, raw = load_usgs_spectrum(sample_path)

    # the sample is put on the SAME wavelength grid as the library
    raw = resample_spectrum(wl, raw, grid)

    return {
        "library": library,
        "mineral_names": mineral_names,
        "grid": grid,
        "raw": raw,
        "sample_path": sample_path,
        "clf": MineralClassifier(model_path)
    }


def analyze(ctx, noise_std=0.0, seed=42):
    """
    Runs the full analysis on the sample.
    noise_std > 0 adds Gaussian noise to the RAW spectrum first
    (same place noise is added during training).
    The same seed always gives the same noise, so a slider value
    always gives the same result.
    """

    raw = ctx["raw"]

    if noise_std and noise_std > 0:

        rng = np.random.default_rng(seed)

        raw = raw + rng.normal(0, noise_std, raw.shape)

    library = ctx["library"]

    mineral_names = ctx["mineral_names"]

    refl = preprocess(raw)

    # --- unmixing + similarity ---
    abundances = FCLS(refl, library)

    sam_scores = np.array([
        SAM(refl, mineral)
        for mineral in library
    ])

    # --- classification ---
    label, confidence, probs = ctx["clf"].predict(refl)

    u = uncertainty(probs)

    # --- reconstruction / anomaly ---
    reconstructed = np.dot(abundances, library)

    loss = reconstruction_loss(refl, reconstructed)

    score = anomaly_score(loss, u)

    # --- interpretation ---
    planet = detect_planetary_origin(abundances, mineral_names)

    geo_ok, geo_message = check_geological_consistency(
        abundances,
        mineral_names
    )

    return {
        "label": label,
        "confidence": confidence,
        "uncertainty": u,
        "loss": loss,
        "anomaly": score,
        "planet": planet,
        "geo_ok": geo_ok,
        "geo_message": geo_message,
        "abundances": abundances,
        "mineral_names": mineral_names,
        "sam_scores": sam_scores,
        "original": refl,
        "reconstructed": reconstructed,
        "wavelength": ctx["grid"]
    }


def run_pipeline(
        sample_path="data/samples/sample.csv",
        model_path="models/random_forest.pkl",
        noise_std=0.0):
    """Convenience: load + analyze in one call."""

    ctx = load_context(sample_path, model_path)

    return analyze(ctx, noise_std)