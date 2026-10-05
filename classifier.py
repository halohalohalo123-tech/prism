import joblib
import numpy as np


class MineralClassifier:

    def __init__(self, model_path):

        self.model = joblib.load(
            model_path
        )

    def predict(self, feature_vector):

        expected = self.model.n_features_in_

        if len(feature_vector) != expected:

            raise ValueError(
                "The model expects %d bands but got %d. "
                "The library changed: run  python train_model.py  "
                "again." % (expected, len(feature_vector))
            )

        probs = self.model.predict_proba(

            feature_vector.reshape(
                1,
                -1
            )

        )[0]

        idx = np.argmax(probs)

        confidence = probs[idx]

        return (

            self.model.classes_[idx],

            confidence,

            probs

        )