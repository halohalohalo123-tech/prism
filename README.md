Planetary Spectral Intelligence System

Overview

This project is an intelligent spectral analysis system for mineral identification and planetary surface interpretation using USGS spectral libraries.

The system combines:

- Spectral preprocessing
- Kubelka-Munk transformation
- Spectral Angle Mapper (SAM)
- Fully Constrained Least Squares (FCLS)
- Random Forest classification
- Anomaly Detection
- Geological Expert Rules
- Planetary Origin Detection
- Interactive NASA-style Dashboard

---

Dataset

USGS Spectral Library

Minerals:

- Quartz
- Kaolinite
- Basalt
- Pyroxene
- Anorthite
- Hematite
- Jarosite

---

Processing Pipeline

Raw Spectrum

↓

Resampling (2152 Bands)

↓

Savitzky-Golay Smoothing

↓

Continuum Removal

↓

Normalization

↓

Kubelka-Munk Transform

↓

FCLS Spectral Unmixing

↓

SAM Similarity

↓

Feature Extraction

↓

Random Forest Classification

↓

Confidence Estimation

↓

Uncertainty Quantification

↓

Reconstruction Loss

↓

Anomaly Detection

↓

Planetary Origin Detection

↓

NASA Dashboard

---

Outputs

- Predicted Mineral
- Mineral Abundance Percentages
- Confidence
- Uncertainty
- Reconstruction Loss
- Anomaly Score
- Geological Consistency
- Planetary Origin

---

Author

Graduation Project

Remote Sensing & Planetary Spectroscopy