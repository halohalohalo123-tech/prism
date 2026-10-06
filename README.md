Planetary Reflectance Intelligent and Synergetic Mechanism

Overview

Mineral identification and abundance estimation from reflectance spectra,
using the USGS spectral library, with an interactive dashboard.

Pipeline:

Raw spectrum (USGS csv)

↓

Cleaning: remove missing values (-1.23e34), rebuild rounded wavelengths

↓

Resampling to the COMMON wavelength grid of the library (1 nm steps)
↓

Savitzky-Golay smoothing

↓

Kubelka-Munk transform  F(R) = (1-R)^2 / 2R   (R clipped to 0.02 - 0.999)

↓

FCLS unmixing (all minerals solved together, abundances >= 0, sum = 1)

↓

SAM similarity

↓

Random Forest classification (trained with noise 0 - 0.05)

↓

Confidence, uncertainty, reconstruction loss, anomaly score

↓

Geological expert rule, planetary-origin heuristic

↓

Dashboard (the noise slider re-runs the whole analysis)

Test results (python evaluate.py)

Classifier, library spectra with new random noise:
- accuracy 100% at noise 0, 0.005, 0.02 and 0.05
- mean confidence 1.00, falling to 0.96 at noise 0.05

Unmixing, 25 random mixtures (error = RMSE of the abundances, 0 = perfect):
- powder mixtures (Kubelka-Munk rule): 0.016 at noise 0,
  0.052 at 0.005, 0.107 at 0.02, 0.158 at 0.05
- side-by-side (patch) mixtures: about 0.20 at every noise level

Samples with known composition:
- Quartz 60 / Kaolinite 40 -> estimated 60 / 40
- Basalt 20 / Hematite 45 / Jarosite 35 -> estimated 18 / 45 / 36
- Anorthite 60 / Pyroxene 40 -> estimated 52 / 40 (+ 7% quartz, not present)

Important notes (limitations)

- Wavelength range: Basalt, Hematite and Jarosite only have data between
  0.37 and 0.83 um in the library files, so the whole system works on the
  range covered by ALL minerals (0.368 - 0.820 um, 453 bands). To use the
  full 0.35 - 2.5 um range, add full-range spectra of these three minerals;
  the range extends automatically (then run train_model.py again).
- The library has ONE spectrum per mineral. The classifier is therefore
  tested for robustness to noise, not for recognising new natural samples.
  The test samples in data/samples/ are mixtures built from the same
  library spectra. Add independent USGS spectra to test recognition.
- data/samples/sample.csv is an exact copy of Quartz.csv, so it always
  gives quartz.
- Continuum removal and min-max normalization were removed from the main
  pipeline: they multiplied the noise by 13-40x and removed the brightness
  and slope information. continuum_removal() is still available in
  preprocessing.py for absorption-band analysis.
- Unmixing uses the Kubelka-Munk mixing model (powders). For patch-like
  (side-by-side) mixtures the abundance error is higher.
- Planetary origin is a simple rule based on which minerals dominate.
- The map card in the dashboard is decorative: it shows a fixed point and
  is not linked to the sample or the results. It needs an internet
  connection to load the map tiles.

Usage

    pip install -r requirements.txt
    python train_model.py          (once, and whenever the library changes)
    python make_test_samples.py    (optional: samples with known composition)
    python evaluate.py             (accuracy and noise tests)
    python main.py                 (analyse data/samples/sample.csv)
    python main.py data/samples/mix_quartz60_kaolinite40.csv

Author

Hala Mohamad Salahi
projsct: Graduation Project in Remote Sensing & Planetary Spectroscopy
institution: IT