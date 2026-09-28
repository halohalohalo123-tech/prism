import pandas as pd
from datetime import datetime


def save_results(
        mineral,
        confidence,
        uncertainty,
        anomaly,
        planet):

    df = pd.DataFrame([{

        "Date": datetime.now(),

        "Mineral": mineral,

        "Confidence": confidence,

        "Uncertainty": uncertainty,

        "Anomaly": anomaly,

        "Planet": planet

    }])

    df.to_csv(

        "results.csv",

        mode="a",

        header=False,

        index=False

    )