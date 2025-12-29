# solow-mrw-growth

Empirical application of the **Solow (1956)** and **Augmented Solow (Mankiw–Romer–Weil, 1992)** growth model to **Germany**, using **World Bank World Development Indicators (WDI)** data and Python.

This project implements the theoretical MRW growth model, calibrates it using observed German data, and evaluates the model’s ability to predict long-run GDP per capita. The repository is structured as a research-grade codebase, prioritizing clarity, modularity, and reproducibility.

---

## Project overview

The repository contains two main components:

1. **Germany analysis pipeline**
   - Fetches WDI data for Germany
   - Constructs MRW variables (investment rate, population growth, initial income)
   - Generates model-based GDP per capita predictions
   - Produces two final figures

2. **Global WDI data fetch (optional)**
   - Downloads a single CSV containing WDI data for all countries
   - Intended for extensions, cross-country analysis, or robustness checks
   - Not required to run the Germany analysis

---

## Repository structure

```
solow-mrw-growth/
├─ scripts/
│  ├─ fetch_wdi_all_countries.py
│  └─ data/
│     └─ wdi_school_pop_gdp_inv_1985_2025.csv
│
├─ src/
│  └─ solow_mrw/
│     ├─ __init__.py
│     ├─ wdi.py
│     ├─ model.py
│     ├─ plots.py
│     ├─ run_germany_analysis.py
│     └─ outputs/
│        └─ figures/
│           ├─ fig_predicted_vs_actual.png
│           └─ fig_prediction_error.png
│
├─ requirements.txt
├─ pyproject.toml
└─ README.md

```

---

## Data sources

All data are obtained programmatically from the **World Bank World Development Indicators (WDI)** API.

Indicators used:
- `NY.GDP.PCAP.KD` — GDP per capita (constant prices)
- `SP.POP.TOTL` — Total population
- `NE.GDI.TOTL.ZS` — Gross capital formation (% of GDP)
- `SE.SEC.ENRR` — Secondary school enrollment (% gross) *(used in the global dataset)*

No manual data cleaning is performed outside the code.

---

## Methodology (high level)

- The Augmented Solow (MRW) model is implemented in closed form.
- Country-specific averages for the investment rate and population growth are computed.
- Long-run GDP per capita is predicted under alternative calibrations:
  - Different values for g + δ
  - Alternative intercepts from Mankiw–Romer–Weil (1992)
- Prediction errors are computed relative to observed GDP per capita.

The focus is **structural, model-based prediction**, not statistical forecasting or machine learning.

---

## How to run the Germany analysis

From the project root directory:

```bash
python -m solow_mrw.run_germany_analysis
```

This will:
- Download WDI data for Germany
- Run the MRW prediction exercise
- Save two figures to:

```
outputs/figures/
├─ fig_predicted_vs_actual.png
└─ fig_prediction_error.png
```

---

## Optional: download WDI data for all countries

This step is **not required** for the Germany analysis.

To generate a global WDI dataset:

```bash
python scripts/fetch_wdi_all_countries.py
```

This creates:

```
scripts/data/wdi_school_pop_gdp_inv_1985_2025.csv
```

The Germany analysis does **not** depend on this file.

---

## Reproducibility

- All data are fetched directly from public APIs.
- No manual intervention is required.
- All outputs (figures and CSVs) are generated programmatically.
- The code is deterministic given the same WDI data.

---

## References

- Solow, R. M. (1956). *A Contribution to the Theory of Economic Growth*.
- Mankiw, N. G., Romer, D., & Weil, D. N. (1992). *A Contribution to the Empirics of Economic Growth*.
- World Bank. *World Development Indicators (WDI)*.

---

## Notes

This repository accompanies an empirical research paper and is intended as a
**research-oriented codebase** focused on clarity, transparency, and reproducibility.

The code implements the Solow–MRW growth model and reproduces the empirical
predictions and figures discussed in the paper.