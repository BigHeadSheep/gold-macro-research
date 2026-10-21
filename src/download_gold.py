
from pathlib import Path
import pandas as pd

# 1. Configuration

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "gold_xauusd.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

START_DATE = "2003-01-01"


# 2. Load gold prices

def load_gold():

    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Gold data not found: {RAW_FILE}")

    df = pd.read_csv(RAW_FILE, comment="#")
    df.columns = df.columns.str.strip().str.lower()

    if not {"date", "close_usd_per_troy_oz"}.issubset(df.columns):
        raise ValueError(f"Unexpected CSV columns: {list(df.columns)}")

    df["date"] = pd.to_datetime(df["date"])
    df["close_usd_per_troy_oz"] = pd.to_numeric(df["close_usd_per_troy_oz"], errors="coerce")

    df = df.set_index("date").sort_index()
    df = df.loc[START_DATE:, ["close_usd_per_troy_oz"]]
    df.index.name = "Date"
    df = df.rename(columns={"close_usd_per_troy_oz": "Gold_USD"})

    if df.empty or df["Gold_USD"].isna().any():
        raise ValueError("Gold data is empty or contains invalid prices.")

    if df.index.has_duplicates or (df["Gold_USD"] <= 0).any():
        raise ValueError("Duplicate dates or non-positive prices found.")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DIR / "gold_prices.csv")

    print(f"Observations: {len(df)}")
    print(f"Start: {df.index.min().date()}")
    print(f"End: {df.index.max().date()}")
    print(df.tail())

    return df


if __name__ == "__main__":
    load_gold()
