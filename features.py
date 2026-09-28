import numpy as np


def build_feature_vector(
        spectrum,
        sam_scores,
        abundances):

    return np.concatenate([

        spectrum,

        sam_scores,

        abundances

    ])