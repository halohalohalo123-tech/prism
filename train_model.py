import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier

from loader import load_usgs_library
from preprocessing import preprocess

# the noise range of the dashboard slider (see dashboard.py)
MAX_NOISE = 0.05
SAMPLES_PER_MINERAL = 500

rng = np.random.default_rng(42)

library, names, grid = load_usgs_library()

print("Library:", names)
print("Bands: %d  (%.3f - %.3f um)" % (len(grid), grid[0], grid[-1]))

X = []
y = []

for mineral, name in zip(library, names):

    for _ in range(SAMPLES_PER_MINERAL):

        # a different noise level for every copy (0 ... MAX_NOISE),
        # added to the RAW spectrum, then the SAME pipeline as runtime
        sigma = rng.uniform(0, MAX_NOISE)

        noisy = mineral + rng.normal(0, sigma, mineral.shape)

        X.append(preprocess(noisy))

        y.append(name)

X = np.array(X)

y = np.array(y)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

joblib.dump(
    model,
    "models/random_forest.pkl"
)

print("Model Saved")