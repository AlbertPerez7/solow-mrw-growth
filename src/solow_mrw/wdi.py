import requests
import pandas as pd


def wdi_download(country_iso3: str, indicator: str, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Download one WDI indicator for one country and return a tidy DataFrame:
    columns: countryiso3code, year, <indicator>
    """
    url = (
        f"https://api.worldbank.org/v2/country/{country_iso3}/indicator/{indicator}"
        f"?format=json&per_page=2000&date={start_year}:{end_year}"
    )

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    js = r.json()
    if not isinstance(js, list) or len(js) < 2 or js[1] is None:
        raise ValueError(f"No data returned for indicator={indicator}, country={country_iso3}")

    df = pd.DataFrame(js[1])[["countryiso3code", "date", "value"]].copy()
    df = df.rename(columns={"date": "year", "value": indicator})
    df["year"] = df["year"].astype(int)
    return df
