import math
import pandas as pd

# OECD coefficients (MRW Table IV, OECD column) — same as your script
BETA_1 = -0.351
BETA_2 = 0.392
BETA_3 = -0.753


def build_germany_dataset(df_pop: pd.DataFrame, df_gdp: pd.DataFrame, df_inv: pd.DataFrame) -> pd.DataFrame:
    """
    Merge the three indicator dataframes into one Germany dataset
    with columns: year, gdp_pc_real, pop, inv_share
    """
    df = df_pop.merge(df_gdp, on=["countryiso3code", "year"], how="outer")
    df = df.merge(df_inv, on=["countryiso3code", "year"], how="outer")

    df = df.rename(columns={
        "SP.POP.TOTL": "pop",
        "NY.GDP.PCAP.KD": "gdp_pc_real",
        "NE.GDI.TOTL.ZS": "inv_share",
    })

    df = df[["year", "gdp_pc_real", "pop", "inv_share"]].sort_values("year").reset_index(drop=True)
    return df


def compute_average_s(df: pd.DataFrame) -> float:
    """Average investment share (inv_share %) converted to s in [0,1]."""
    return (df["inv_share"] / 100.0).mean()


def compute_average_n(df: pd.DataFrame, start_year: int, end_year: int) -> float:
    """Average annual log population growth between start and end."""
    pop_0 = df.loc[df["year"] == start_year, "pop"].values[0]
    pop_T = df.loc[df["year"] == end_year, "pop"].values[0]
    T = end_year - start_year
    return (math.log(pop_T) - math.log(pop_0)) / T


def predict_yT(y0: float, s: float, n: float, g_delta: float, C_used: float) -> float:
    """
    MRW-style growth regression prediction:
    ln(y_T) - ln(y_0) = C + β1 ln(y0) + β2 ln(s) + β3 ln(n+g+δ)
    """
    growth_log = (
        C_used
        + BETA_1 * math.log(y0)
        + BETA_2 * math.log(s)
        + BETA_3 * math.log(n + g_delta)
    )
    ln_yT = math.log(y0) + growth_log
    return math.exp(ln_yT)


def compute_errors(actual: float, predicted_list: list[float]) -> list[float]:
    """Percent error = (Actual − Predicted) / Predicted * 100."""
    return [(actual - p) / p * 100.0 for p in predicted_list]
