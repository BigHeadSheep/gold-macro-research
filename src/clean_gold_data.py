
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "gold_prices.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "gold_daily.csv"


def clean_gold_data():

    df = pd.read_csv(INPUT_FILE, parse_dates=["Date"], index_col="Date")
    df = df.sort_index()

    # Exclude weekends
    df = df[df.index.dayofweek < 5].copy()

    # Validate observations
    if df.index.has_duplicates:
        raise ValueError("Duplicate dates found.")

    if df["Gold_USD"].isna().any() or (df["Gold_USD"] <= 0).any():
        raise ValueError("Missing or invalid gold prices found.")

    # Calculate log returns between consecutive available weekdays
    df["Gold_Log_Return"] = np.log(df["Gold_USD"]).diff()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE)

    print("--- Cleaned Gold Dataset ---")
    print(f"Observations: {len(df)}")
    print(f"Start: {df.index.min().date()}")
    print(f"End: {df.index.max().date()}")

    print("\nSummary statistics:")
    print(df.describe())

    print(f"\nSaved to: {OUTPUT_FILE}")

    return df


if __name__ == "__main__":
    clean_gold_data()
