
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "gold_prices.csv"

df = pd.read_csv(DATA_FILE, parse_dates=["Date"], index_col="Date")

print("\n--- Gold Data Quality Report ---")

print(f"Observations: {len(df)}")
print(f"Start date: {df.index.min().date()}")
print(f"End date: {df.index.max().date()}")

# Weekend observations
weekends = df[df.index.dayofweek >= 5]
print(f"\nWeekend observations: {len(weekends)}")

# Consecutive unchanged prices
unchanged = df["Gold_USD"].eq(df["Gold_USD"].shift())
print(f"Consecutive unchanged prices: {unchanged.sum()}")

# Missing values
print("\nMissing values:")
print(df.isna().sum())

# Check duplicate dates
print(f"\nDuplicate dates: {df.index.duplicated().sum()}")

# Daily log returns, restricted to weekdays
weekday_data = df[df.index.dayofweek < 5].copy()
weekday_data["Return"] = (
    weekday_data["Gold_USD"] / weekday_data["Gold_USD"].shift()
).apply("log") if False else None

# Calculate returns with numpy
import numpy as np

weekday_data["Log_Return"] = np.log(weekday_data["Gold_USD"]).diff()

print("\nLargest absolute daily log returns:")
print(weekday_data["Log_Return"].abs().nlargest(10))
