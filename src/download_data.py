
from datetime import date
from pathlib import Path

import pandas as pd
from pandas_datareader import data as web


# --------------------------------------------------
# 1. Project configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

START_DATE = "2003-01-01"
END_DATE = date.today().isoformat()

FRED_SERIES = {
    "DGS2": "US_2Y_Nominal",
    "DGS10": "US_10Y_Nominal",
    "DGS30": "US_30Y_Nominal",
    "DFII10": "US_10Y_Real",
    "DFII30": "US_30Y_Real",
    "T10YIE": "US_10Y_Breakeven",
}


# --------------------------------------------------
# 2. Download FRED data
# --------------------------------------------------

def download_fred_data():

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    datasets = []

    for series_id, column_name in FRED_SERIES.items():

        print(f"Downloading {series_id}...")

        df = web.DataReader(series_id,"fred", START_DATE, END_DATE)

        df.index.name = "Date"

        # Save original FRED series
        df.to_csv(RAW_DIR / f"{series_id}.csv")

        # Rename for consolidated dataset
        df = df.rename(columns={series_id: column_name})

        datasets.append(df)

    # Merge all data using dates
    combined = pd.concat(datasets, axis=1)
    combined = combined.sort_index()

    output_file = PROCESSED_DIR / "us_treasury_yields.csv"

    combined.to_csv(output_file)

    print("\nDownload completed!")
    print(f"Saved to: {output_file}")

    return combined


# --------------------------------------------------
# 3. Data quality checks
# --------------------------------------------------

def check_data(df):

    print("\n--- Dataset overview ---")

    print(f"Start date: {df.index.min().date()}")
    print(f"End date:   {df.index.max().date()}")

    print(f"\nObservations: {len(df)}")

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nFirst observations:")
    print(df.head())

    print("\nLast observations:")
    print(df.tail())

    print("\nSummary statistics:")
    print(df.describe())


# --------------------------------------------------
# 4. Main
# --------------------------------------------------

if __name__ == "__main__":

    data = download_fred_data()

    check_data(data)
