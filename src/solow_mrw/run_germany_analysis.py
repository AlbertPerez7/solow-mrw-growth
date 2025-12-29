from pathlib import Path

from solow_mrw.model import (
    build_germany_dataset,
    compute_average_s,
    compute_average_n,
    predict_yT,
    compute_errors,
)
from solow_mrw.plots import plot_predicted_vs_actual, plot_errors
from solow_mrw.wdi import wdi_download


# --------- PARAMETERS ---------
START_YEAR = 1985
END_YEAR = 2024
COUNTRY_ISO3 = "DEU"

INDICATOR_POP = "SP.POP.TOTL"
INDICATOR_GDP_PC = "NY.GDP.PCAP.KD"
INDICATOR_INV = "NE.GDI.TOTL.ZS"

# OECD coefficients (Table IV)
C = 2.19
C_2 = 2.45  # alternative c (robustness)

G_PLUS_DELTA_1 = 0.05
G_PLUS_DELTA_2 = 0.035  # alternative (robustness)


def main() -> None:
    print("=== Downloading WDI data for Germany (DEU) ===")

    df_pop = wdi_download(COUNTRY_ISO3, INDICATOR_POP, START_YEAR, END_YEAR)
    df_gdp = wdi_download(COUNTRY_ISO3, INDICATOR_GDP_PC, START_YEAR, END_YEAR)
    df_inv = wdi_download(COUNTRY_ISO3, INDICATOR_INV, START_YEAR, END_YEAR)

    df = build_germany_dataset(df_pop, df_gdp, df_inv)

    # Compute s and n
    s = compute_average_s(df)
    n = compute_average_n(df, START_YEAR, END_YEAR)

    # Initial and actual income
    y0 = df.loc[df["year"] == START_YEAR, "gdp_pc_real"].values[0]
    y_real = df.loc[df["year"] == END_YEAR, "gdp_pc_real"].values[0]

    # 3 prediction cases (same as your original)
    y_A = predict_yT(y0, s, n, G_PLUS_DELTA_1, C)      # baseline
    y_B = predict_yT(y0, s, n, G_PLUS_DELTA_2, C)      # alt g+δ
    y_C = predict_yT(y0, s, n, G_PLUS_DELTA_1, C_2)    # alt c

    predicted_vals = [y_A, y_B, y_C]
    errors = compute_errors(y_real, predicted_vals)

    print("\n=== PARAMETERS ===")
    print(f"y_{START_YEAR} = {y0:.2f}")
    print(f"s            = {s:.6f}")
    print(f"n            = {n:.6f}")
    print(f"Actual y_{END_YEAR} = {y_real:.2f}")

    print("\n=== RESULTS ===")
    print(f"Case A (C=2.19, g+δ=0.05):  Pred={y_A:.2f},  Error={errors[0]:.2f}%")
    print(f"Case B (C=2.19, g+δ=0.035): Pred={y_B:.2f},  Error={errors[1]:.2f}%")
    print(f"Case C (C=2.45, g+δ=0.05):  Pred={y_C:.2f},  Error={errors[2]:.2f}%")

    # ---- Figures (only 2) ----
    out_fig = Path("outputs/figures")
    out_fig.mkdir(parents=True, exist_ok=True)

    labels = [
        "A: C=2.19, g+δ=0.05",
        "B: C=2.19, g+δ=0.035",
        "C: C=2.45, g+δ=0.05",
    ]

    plot_predicted_vs_actual(
        labels=labels,
        predicted_vals=predicted_vals,
        actual_vals=[y_real, y_real, y_real],
        output_path=str(out_fig / "fig_predicted_vs_actual.png"),
    )

    plot_errors(
        labels=labels,
        errors=errors,
        output_path=str(out_fig / "fig_prediction_error.png"),
    )

    print("\nSaved figures to outputs/figures/")


if __name__ == "__main__":
    main()
