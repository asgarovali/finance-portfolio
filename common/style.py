"""One chart style for the whole portfolio."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

# dark blue first, then muted colours; grey is kept for benchmarks / reference lines
PALETTE = ["#1f3b5c", "#c0504d", "#7f9f4f", "#d49a3a", "#6b5b95", "#4f8fbf"]
GREY = "#8c8c8c"


def use_style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#e5e5e5",
        "grid.linewidth": 0.6,
        "axes.prop_cycle": plt.cycler(color=PALETTE),
        "legend.frameon": False,
        "figure.figsize": (8, 4.5),
        "figure.dpi": 100,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    })


def add_source(fig: plt.Figure, text: str) -> None:
    """Source line under the chart, e.g. 'Source: FRED, series DGS10, retrieved 2026-10-22'."""
    fig.text(0.01, -0.02, text, fontsize=8, color=GREY, ha="left", va="top")


def save(fig: plt.Figure, name: str, out_dir: str | Path = "outputs/figures") -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.png"
    fig.savefig(path, dpi=200)
    return path
