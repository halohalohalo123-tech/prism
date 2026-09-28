import numpy as np

from loader import *

from preprocessing import *

from unmixing import *

from similarity import *

from features import *

from classifier import *

from anomaly import *

from planetary import *

from expert_system import *

from dashboard import *

from results import *

# =====================================
# LOAD LIBRARY
# =====================================

library, mineral_names = load_usgs_library()


# =====================================
# LOAD SAMPLE
# =====================================

sample_path = "data/samples/sample.csv"

wl, refl = load_usgs_spectrum(
    sample_path
)

wl, refl = resample_spectrum(
    wl,
    refl
)


# =====================================
# PREPROCESSING
# =====================================

refl = smooth_signal(
    refl
)

refl = continuum_removal(
    refl
)

refl = normalize_spectrum(
    refl
)

refl = kubelka_munk(
    refl
)


# =====================================
# FCLS
# =====================================

abundances = FCLS(
    refl,
    library
)


# =====================================
# SAM
# =====================================

sam_scores = np.array([

    SAM(
        refl,
        mineral
    )

    for mineral in library

])


# =====================================
# FEATURE VECTOR
# =====================================

feature_vector = build_feature_vector(

    refl,

    sam_scores,

    abundances

)


# =====================================
# RANDOM FOREST
# =====================================

clf = MineralClassifier(

    "models/random_forest.pkl"

)

label, confidence, probs = clf.predict(refl)


# =====================================
# UNCERTAINTY
# =====================================

u = uncertainty(
    probs
)


# =====================================
# RECONSTRUCTION
# =====================================

reconstructed = np.dot(

    abundances,

    library

)


loss = reconstruction_loss(

    refl,

    reconstructed

)


score = anomaly_score(

    loss,

    u

)


# =====================================
# PLANETARY DETECTOR
# =====================================

planet = detect_planetary_origin(

    abundances,

    mineral_names

)


# =====================================
# GEOLOGICAL RULES
# =====================================

geo_ok, geo_message = check_geological_consistency(

        abundances,

        mineral_names

    )


# =====================================
# RESULTS
# =====================================

print()

print("========== RESULT ==========")

print()

print("Predicted Mineral:")
print(label)

print()

print("Confidence:")
print(round(confidence, 4))

print()

print("Uncertainty:")
print(round(u, 4))

print()

print("Reconstruction Loss:")
print(round(loss, 6))

print()

print("Anomaly Score:")
print(round(score, 6))

print()

print("Planetary Origin:")
print(planet)

print()

print("Geological Consistency:")
print(geo_message)

print()

print("Abundances:")

for name, abundance in zip(

        mineral_names,

        abundances):

    print(

        f"{name}: "

        f"{abundance*100:.2f}%"

    )


save_results(

    label,

    confidence,

    u,

    score,

    planet

)


launch_dashboard(

    mineral=label,

    confidence=confidence,

    uncertainty=u,

    anomaly=score,

    abundances=abundances,

    mineral_names=mineral_names,

    original=refl,

    reconstructed=reconstructed,

    planet=planet,

    geo_message=geo_message

)

