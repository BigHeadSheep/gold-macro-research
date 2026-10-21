from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, FixedLocator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "gold_daily.csv"
FIGURE_DIR = PROJECT_ROOT / "figures"

def thousands(x, pos):
    return f"{int(x):,}" if x >= 1000 else f"{int(x)}"

def style_axis(ax, ylabel):
    ax.set_xlabel("")
    ax.set_ylabel(ylabel, fontsize=11, color="0.15")
    ax.grid(axis="y", color="0.85", linewidth=0.8)
    ax.grid(axis="x", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("0.20")
    ax.spines["bottom"].set_color("0.20")
    ax.spines["left"].set_linewidth(0.9)
    ax.spines["bottom"].set_linewidth(0.9)
    ax.tick_params(axis="both", labelsize=10, colors="0.20", length=4, width=0.8)
    ax.xaxis.set_major_locator(mdates.YearLocator(3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.margins(x=0.01)

def save_figure(fig, name):
    fig.savefig(FIGURE_DIR / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIGURE_DIR / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

def plot_linear(df):
    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    ax.plot(df.index, df["Gold_USD"], color="0.15", linewidth=1.35)
    style_axis(ax, "USD per troy ounce")
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    fig.tight_layout()
    save_figure(fig, "gold_price_linear")

def plot_log(df):
    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    ax.plot(df.index, df["Gold_USD"], color="0.15", linewidth=1.35)
    ax.set_yscale("log")
    style_axis(ax, "USD per troy ounce")
    ticks = [300, 400, 600, 1000, 2000, 3000, 4000, 6000]
    ax.yaxis.set_major_locator(FixedLocator(ticks))
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    fig.tight_layout()
    save_figure(fig, "gold_price_log")

def plot_gold():
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "Times", "DejaVu Serif"]
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"
    plt.rcParams["savefig.facecolor"] = "white"
    plt.rcParams["axes.edgecolor"] = "0.20"
    plt.rcParams["axes.linewidth"] = 0.9
    plt.rcParams["xtick.color"] = "0.20"
    plt.rcParams["ytick.color"] = "0.20"
    plt.rcParams["text.color"] = "0.15"
    plt.rcParams["axes.labelcolor"] = "0.15"
    plt.rcParams["font.size"] = 10

    df = pd.read_csv(DATA_FILE, parse_dates=["Date"], index_col="Date")
    df = df.sort_index()

    plot_linear(df)
    plot_log(df)

    print("Figures saved to:", FIGURE_DIR)
    print("Created: gold_price_linear.pdf/.png")
    print("Created: gold_price_log.pdf/.png")

if __name__ == "__main__":
    plot_gold()