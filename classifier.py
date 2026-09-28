import joblib
import numpy as np


class MineralClassifier:

    def __init__(self, model_path):

        self.model = joblib.load(
            model_path
        )

    def predict(self, feature_vector):

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