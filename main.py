import sys

from pipeline import load_context, analyze
from dashboard import launch_dashboard
from results import save_results


# optional: python main.py data/samples/other_sample.csv
sample = sys.argv[1] if len(sys.argv) > 1 else "data/samples/sample.csv"

ctx = load_context(sample)

r = analyze(ctx)


# =====================================
# RESULTS
# =====================================

print()
print("========== RESULT ==========")
print()

print("Predicted Mineral:")
print(r["label"])
print()

print("Confidence:")
print(round(r["confidence"], 4))
print()

print("Uncertainty:")
print(round(r["uncertainty"], 4))
print()

print("Reconstruction Loss:")
print(round(r["loss"], 6))
print()

print("Anomaly Score:")
print(round(r["anomaly"], 6))
print()

print("Planetary Origin:")
print(r["planet"])
print()

print("Geological Consistency:")
print(r["geo_message"])
print()

print("Abundances:")

for name, abundance in zip(
        r["mineral_names"],
        r["abundances"]):

    print(f"{name}: {abundance * 100:.2f}%")


save_results(
    r["label"],
    r["confidence"],
    r["uncertainty"],
    r["anomaly"],
    r["planet"]
)


launch_dashboard(ctx)