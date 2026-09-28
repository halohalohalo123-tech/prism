import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier

from loader import *


library, names = load_usgs_library()

X = []
y = []


for mineral, name in zip(
        library,
        names):

    for _ in range(500):

        noise = np.random.normal(

            0,

            0.005,

            mineral.shape

        )

        sample = mineral + noise

        X.append(sample)

        y.append(name)


X = np.array(X)

y = np.array(y)


model = RandomForestClassifier(

    n_estimators=300,

    random_state=42

)

model.fit(X, y)

joblib.dump(

    model,

    "models/random_forest.pkl"

)

print("Model Saved")