import requests
import pandas as pd
from pathlib import Path

# =========================
# PARAMETERS
# =========================
START_YEAR = 1985
END_YEAR = 2025

# WDI indicators (Solow / MRW)
INDICATOR_SCHOOL = "SE.SEC.ENRR"      # Secondary school enrollment (% gross)
INDICATOR_POP = "SP.POP.TOTL"         # Total population
INDICATOR_GDP_PC = "NY.GDP.PCAP.KD"   # GDP per capita (constant prices)
INDICATOR_INV = "NE.GDI.TOTL.ZS"      # Gross capital formation (% of GDP)

# 👉 CSV directly in /data
OUT_DIR = Path("data")
OUT_FILE = OUT_DIR / f"wdi_school_pop_gdp_inv_{START_YEAR}_{END_YEAR}.csv"


# =========================
# HELPERS
# =========================
def _extract_country_name(country):
    if isinstance(country, dict):
        return country.get("value")
    return country


def wdi_download_all(indicator: str, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Download one WDI indicator for ALL countries.
    Returns a tidy DataFrame with:
    country_name, countryiso3code, year, <indicator>
    """
    url = (
        f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
        f"?format=json&per_page=20000&date={start_year}:{end_year}"
    )

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    js = r.json()
    if not isinstance(js, list) or len(js) < 2 or js[1] is None:
        raise ValueError(f"No data returned for indicator {indicator}")

    df = pd.DataFrame(js[1])
    df["country_name"] = df["country"].apply(_extract_country_name)

    df = df[["country_name", "countryiso3code", "date", "value"]].copy()
    df = df.rename(columns={"date": "year", "value": indicator})
    df["year"] = df["year"].astype(int)

    # Keep only real countries (exclude aggregates)
    df = df[df["countryiso3code"].notna()]
    df = df[df["countryiso3code"].str.len() == 3]

    return df


# =========================
# MAIN
# =========================
def main() -> None:
    print("=== Fetching WDI data for ALL countries ===")
    print(f"Years: {START_YEAR}–{END_YEAR}")

    df_school = wdi_download_all(INDICATOR_SCHOOL, START_YEAR, END_YEAR).rename(
        columns={INDICATOR_SCHOOL: "school"}
    )
    df_pop = wdi_download_all(INDICATOR_POP, START_YEAR, END_YEAR).rename(
        columns={INDICATOR_POP: "pop"}
    )
    df_gdp = wdi_download_all(INDICATOR_GDP_PC, START_YEAR, END_YEAR).rename(
        columns={INDICATOR_GDP_PC: "gdp_pc_real"}
    )
    df_inv = wdi_download_all(INDICATOR_INV, START_YEAR, END_YEAR).rename(
        columns={INDICATOR_INV: "inv_share"}
    )

    print("Downloaded rows:")
    print("  school:", len(df_school))
    print("  pop   :", len(df_pop))
    print("  gdp   :", len(df_gdp))
    print("  inv   :", len(df_inv))

    # Merge on (countryiso3code, year)
    df = df_school.merge(
        df_pop[["countryiso3code", "year", "pop"]],
        on=["countryiso3code", "year"],
        how="outer",
    )
    df = df.merge(
        df_gdp[["countryiso3code", "year", "gdp_pc_real"]],
        on=["countryiso3code", "year"],
        how="outer",
    )
    df = df.merge(
        df_inv[["countryiso3code", "year", "inv_share"]],
        on=["countryiso3code", "year"],
        how="outer",
    )

    df = df.sort_values(["countryiso3code", "year"]).reset_index(drop=True)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)

    print(f"\n✅ Saved CSV to: {OUT_FILE}")
    print("=== Done ===")


if __name__ == "__main__":
    main()
